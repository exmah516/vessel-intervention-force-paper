"""Figure A revision: existing samples/parameters, 76 x 112 mm, 9 pt.

Panel (a): cycle 20261024_223855_c09, elapsed time from motion onset.
Panel (b): all 113 external-holdout cycles, without selection or smoothing.
Run with Python; outputs beside this script are created exclusively.
"""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\Sui\.codex\skills\nature-figure\scripts")
from audit_panel_alignment import require_matplotlib_panel_alignment


BASE = Path(r"D:\Work_files\Vessel intervention Robot\paper\outputs\paper_selected_results_20261104")
V4 = Path(r"D:\Work_files\Vessel intervention Robot\paper\outputs\axial_recovery_audit_20261102\continuous_targets_20261102_v4_local")
COLORS = {"measured": "#333333", "friction_only": "#B07C4F",
          "single": "#0072B2", "double": "#009E73"}


def relaxation(s, amplitude, delta, lam, dc):
    if abs(dc - lam) < 1e-5 * max(dc, lam):
        return (amplitude - delta * s / lam) * np.exp(-s / lam)
    return (amplitude * np.exp(-s / lam)
            - delta * dc / (dc - lam) * (np.exp(-s / dc) - np.exp(-s / lam)))


def build_figure(cycle, a):
    fonts = {name: font_manager.findfont(name, fallback_to_default=False)
             for name in ("SimSun", "Times New Roman")}
    plt.rcParams.update({
        "font.family": ["Times New Roman", "SimSun"],
        "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 9,
        "ytick.labelsize": 9, "legend.fontsize": 9,
        "mathtext.fontset": "stix", "axes.unicode_minus": False,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "axes.linewidth": .6, "lines.linewidth": .9,
        "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False,
    })
    b = pd.read_csv(BASE / "source_data/figureA_b.csv")
    frozen = json.loads((V4 / "physical_parameters_frozen.json").read_text(encoding="utf-8"))["077"]
    x, measured = a.s_rec_mm.to_numpy(), a.measured_N.to_numpy()
    enabled = a.raw_row.to_numpy() >= int(cycle.onset_row)
    s = x[enabled] - cycle.branch_shift_mm
    latch, amplitude = float(cycle.D_N), float(cycle.A_N)
    assert len(a) > 2 and np.all(np.diff(x) >= -1e-8)
    assert np.array_equal(a.raw_row, np.arange(int(cycle.motion_onset_row), int(cycle.motion_onset_row) + len(a)))
    assert np.array_equal(enabled, a.elastic_loading_only_N.notna().to_numpy())
    assert abs(s[0]) < 1e-10 and np.allclose(a.D_N, latch, rtol=0, atol=1e-10)

    # Retain the existing complete-model output exactly, including its initial hold.
    complete = a.recovery_model_compensated_output_N.to_numpy()
    k0, full_dc, bf = frozen["physical"]
    full_delta = bf * np.log1p(cycle.v1_mm_s * cycle.t_h_s / full_dc) * np.exp(-cycle.branch_shift_mm / full_dc)
    full_lam = (amplitude + full_delta) / k0
    np.testing.assert_allclose(complete[enabled], measured[enabled] + relaxation(s, amplitude, full_delta, full_lam, full_dc), rtol=0, atol=1e-10)
    assert len(complete) == len(a) and np.isfinite(complete).all()
    np.testing.assert_allclose(complete[:np.flatnonzero(enabled)[0] + 1], latch, rtol=0, atol=1e-10)

    elapsed = a.time_s.to_numpy() - float(a.time_s.iloc[0])
    assert len(a) == 531 and elapsed[0] == 0 and np.all(np.diff(elapsed) > 0)
    fig, axs = plt.subplots(2, 1, figsize=(76 / 25.4, 112 / 25.4))
    fig.subplots_adjust(left=.19, right=.975, bottom=.155, top=.84, hspace=.95)
    ax = axs[0]
    raw, = ax.plot(elapsed, measured, color=COLORS["measured"], lw=.65,
                   drawstyle="steps-post", label="原始数据")
    full, = ax.plot(elapsed, complete, color=COLORS["double"], ls="-.", label="完整物理模型补偿",
                   marker="s", markevery=max(1, len(a) // 10), ms=2.2, mfc="none", mew=.6)
    bar = ax.axhline(latch, color="#777777", ls=(0, (3, 2)), lw=.7, label=r"$\bar{F}$")
    fig.legend(handles=[raw, full, bar], loc="upper center",
               bbox_to_anchor=(.52, .985), ncol=3, columnspacing=.8,
               handlelength=1.6, handletextpad=.45, labelspacing=.35, borderaxespad=0)
    ax.set_ylabel("轴向力/N", labelpad=3)
    xlabel = HPacker(children=[
        TextArea("推进时间", textprops={"fontfamily": "SimSun", "fontsize": 9}),
        TextArea("/s", textprops={"fontfamily": "Times New Roman", "fontsize": 9}),
    ], align="center", pad=0, sep=0)
    ax.add_artist(AnnotationBbox(xlabel, (.5, -.31), xycoords=ax.transAxes,
                  box_alignment=(.5, 1), frameon=False, pad=0))
    ax.margins(x=.025, y=.12)
    ax.set_xlim(left=0)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    fig.text(.5825, .46, "(a) 典型重加载阶段的补偿效果", ha="center", va="center", fontsize=9)

    ax = axs[1]
    methods = ["measured", "friction_only", "single", "double"]
    groups = [b[b.model_id == method].sort_values("cycle_id") for method in methods]
    assert len(b) == 4 * 113 and b.run_id.nunique() == 15
    for group in groups:
        assert len(group) == 113 and group.cycle_id.nunique() == 113
        assert np.isfinite(group.RMSE_N).all()
        assert group.cycle_id.tolist() == groups[0].cycle_id.tolist()
    data = [group.RMSE_N.to_numpy() for group in groups]
    box_width = .34
    boxes = ax.boxplot(data, positions=[1, 2, 3, 4], widths=box_width, patch_artist=True, showfliers=False,
        medianprops={"color": "#222222", "linewidth": .9},
        whiskerprops={"linewidth": .8}, capprops={"linewidth": .8})
    for i, method in enumerate(methods):
        color = COLORS[method]
        boxes["boxes"][i].set(facecolor=color, edgecolor=color, alpha=.25)
        for artist in boxes["whiskers"][2*i:2*i+2] + boxes["caps"][2*i:2*i+2]:
            artist.set_color(color)
    rng = np.random.default_rng(20261102)
    for position, (values, method) in enumerate(zip(data, methods), start=1):
        scatter_x = position - .34 + rng.uniform(-.13, .13, len(values))
        assert np.all((scatter_x > position - .5) & (scatter_x < position - box_width / 2))
        points = ax.scatter(scatter_x, values,
                            s=7, color=COLORS[method], alpha=.4, linewidths=0, zorder=3)
        assert len(points.get_offsets()) == 113
    ax.set_xticks([1, 2, 3, 4], ["校正测量", "仅附加\n摩擦", "仅弹性\n加载", "完整恢复\n模型"])
    ax.set_ylabel("误差/N", labelpad=3)
    ax.margins(y=.12)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    fig.text(.5825, .04, "(b) 不同模型形式的S9阶段误差分布", ha="center", va="center", fontsize=9)
    for ax in axs:
        ax.tick_params(axis="both", width=.6, length=2.5, pad=2)
    fig.canvas.draw()
    np.testing.assert_allclose(axs[0].get_position().bounds[::2], axs[1].get_position().bounds[::2], rtol=0, atol=1e-12)
    stats = {
        "cycle_id": cycle.cycle_id, "samples_a": len(a), "time_range_s": [float(elapsed[0]), float(elapsed[-1])], "cycles_b_per_method": {m: len(g) for m, g in zip(methods, groups)},
        "activation_mm": float(cycle.branch_shift_mm), "latch_N": latch,
        "jitter_seed": 20261102, "size_mm": [76, 112], "font_pt": 9, "fonts": fonts,
    }
    return fig, stats


def save_figure(fig, prefix):
    paths = [prefix.with_suffix(ext) for ext in (".pdf", ".png")]
    for path in paths:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite: {path}")
    for path in paths:
        with path.open("xb") as handle:
            fig.savefig(handle, format=path.suffix[1:], dpi=600)




if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    prefix = Path(__file__).with_suffix("")
    if any(prefix.with_suffix(ext).exists() for ext in (".pdf", ".png")):
        raise FileExistsError("Output already exists; refusing to overwrite.")
    a = pd.read_csv(BASE.parent / "figureA_recovery_candidates_20261105/source_data/20261024_223855_c09.csv")
    manifest = pd.read_csv(V4 / "cycle_manifest.csv", dtype={"branch": str})
    rows = manifest[(manifest.branch == "077") & (manifest.cycle_id == "20261024_223855_c09")]
    assert len(rows) == 1
    fig, stats = build_figure(rows.iloc[0], a)
    require_matplotlib_panel_alignment(
        fig, json_out=prefix.with_suffix(".alignment.json"), strict=True)
    save_figure(fig, prefix)
    plt.close(fig)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
