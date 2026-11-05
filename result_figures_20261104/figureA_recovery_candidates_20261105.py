"""Figure A revision: existing samples/parameters, 76 x 112 mm, 9 pt.

Panel (a): three selected external-holdout cycles, one figure per cycle.
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


BASE = Path(r"D:\Work_files\Vessel intervention Robot\paper\outputs\paper_selected_results_20261104")
V4 = Path(r"D:\Work_files\Vessel intervention Robot\paper\outputs\axial_recovery_audit_20261102\continuous_targets_20261102_v4_local")
ORIGINAL_CYCLE = "20261024_223712_c07"
NET = BASE.parent / "continuous_feedback_retrain6_no_wait_srec_direction_repeat_20261103"
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
    friction = json.loads((BASE / "friction_only_fit.json").read_text(encoding="utf-8"))
    x, measured = a.s_rec_mm.to_numpy(), a.measured_N.to_numpy()
    enabled = a.raw_row.to_numpy() >= int(cycle.onset_row)
    s = x[enabled] - cycle.branch_shift_mm
    latch, amplitude = float(cycle.D_N), float(cycle.A_N)
    assert len(a) > 2 and np.all(np.diff(x) >= -1e-8)
    assert np.array_equal(a.raw_row, np.arange(int(cycle.motion_onset_row), int(cycle.motion_onset_row) + len(a)))
    assert np.array_equal(enabled, a.elastic_loading_only_N.notna().to_numpy())
    assert abs(s[0]) < 1e-10 and np.allclose(a.D_N, latch, rtol=0, atol=1e-10)

    elastic = np.full(len(a), latch)
    elastic[enabled] = measured[enabled] + amplitude * np.exp(-s / frozen["single"][0])
    np.testing.assert_allclose(elastic[enabled],
        measured[enabled] + latch - a.elastic_loading_only_N.to_numpy()[enabled], rtol=0, atol=1e-10)
    friction_output = np.full(len(a), latch)
    delta, dc = friction["parameters"]
    friction_output[enabled] = measured[enabled] + relaxation(s, amplitude, delta, friction["lambda_fixed_mm"], dc)

    # Retain the existing complete-model output exactly, including its initial hold.
    complete = a.recovery_model_compensated_output_N.to_numpy()
    k0, full_dc, bf = frozen["physical"]
    full_delta = bf * np.log1p(cycle.v1_mm_s * cycle.t_h_s / full_dc) * np.exp(-cycle.branch_shift_mm / full_dc)
    full_lam = (amplitude + full_delta) / k0
    np.testing.assert_allclose(complete[enabled], measured[enabled] + relaxation(s, amplitude, full_delta, full_lam, full_dc), rtol=0, atol=1e-10)
    for values in (friction_output, elastic, complete):
        assert len(values) == len(a) and np.isfinite(values).all()
        np.testing.assert_allclose(values[:np.flatnonzero(enabled)[0] + 1], latch, rtol=0, atol=1e-10)

    fig, axs = plt.subplots(2, 1, figsize=(76 / 25.4, 112 / 25.4))
    fig.subplots_adjust(left=.19, right=.975, bottom=.155, top=.84, hspace=.95)
    ax = axs[0]
    raw, = ax.plot(x, measured, color=COLORS["measured"], lw=.65,
                   drawstyle="steps-post", label="原始数据")
    fr, = ax.plot(x, friction_output, color=COLORS["friction_only"], ls=":", label="仅附加摩擦补偿")
    el, = ax.plot(x, elastic, color=COLORS["single"], ls="--", label="仅弹性加载补偿")
    full, = ax.plot(x, complete, color=COLORS["double"], ls="-.", label="完整物理模型补偿",
                   marker="s", markevery=max(1, len(a) // 10), ms=2.2, mfc="none", mew=.6)
    bar = ax.axhline(latch, color="#777777", ls=(0, (3, 2)), lw=.7, label=r"$\bar{F}$")
    # Matplotlib fills columns; this ordering gives the requested row-wise legend.
    fig.legend(handles=[raw, el, bar, fr, full], loc="upper center",
               bbox_to_anchor=(.52, .985), ncol=2, columnspacing=.65,
               handlelength=1.6, handletextpad=.45, labelspacing=.35, borderaxespad=0)
    ax.set_ylabel("轴向力/N", labelpad=3)
    xlabel = HPacker(children=[
        TextArea("推进行程", textprops={"fontfamily": "SimSun", "fontsize": 9}),
        TextArea(r"$s_{\mathrm{r}}$/mm", textprops={"fontfamily": "Times New Roman", "fontsize": 9}),
    ], align="center", pad=0, sep=2)
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
    boxes = ax.boxplot(data, positions=[1, 2, 3, 4], widths=.48, patch_artist=True, showfliers=False,
        medianprops={"color": "#222222", "linewidth": .9},
        whiskerprops={"linewidth": .8}, capprops={"linewidth": .8})
    for i, method in enumerate(methods):
        color = COLORS[method]
        boxes["boxes"][i].set(facecolor=color, edgecolor=color, alpha=.25)
        for artist in boxes["whiskers"][2*i:2*i+2] + boxes["caps"][2*i:2*i+2]:
            artist.set_color(color)
    rng = np.random.default_rng(20261102)
    for position, (values, method) in enumerate(zip(data, methods), start=1):
        points = ax.scatter(position + rng.uniform(-.14, .14, len(values)), values,
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
        "cycle_id": cycle.cycle_id, "samples_a": len(a), "cycles_b_per_method": {m: len(g) for m, g in zip(methods, groups)},
        "activation_mm": float(cycle.branch_shift_mm), "latch_N": latch,
        "friction_lambda_mm": friction["lambda_fixed_mm"], "friction_delta_N": delta, "friction_dc_mm": dc,
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




def read_manifest():
    frame = pd.read_csv(V4 / "cycle_manifest.csv", dtype={"branch": str})
    frame = frame[(frame.branch == "077") & (frame.role == "external_holdout")]
    assert len(frame) == 113 and frame.run_id.nunique() == 15
    return frame.set_index("cycle_id", drop=False)


def cycle_data(cycle, cache):
    if cycle.run_id not in cache:
        with np.load(NET / "predictions" / f"{cycle.run_id}__full.npz") as z:
            cache[cycle.run_id] = {k: z[k] for k in ("time", "position", "force", "reference", "physical")}
    f = cache[cycle.run_id]
    start, motion = int(cycle.onset_row), int(cycle.motion_onset_row)
    rows = np.arange(start, int(cycle.end_row) + 1)
    position = f["position"][rows]
    s = np.sign(position[-1] - position[0]) * (position - position[0])
    keep = (s >= 0) & (s <= cycle.valid_end_mm + 1e-9)
    rows, s = rows[keep], s[keep]
    indices = np.r_[np.arange(motion, start), rows]
    x = abs(f["position"][indices] - f["position"][motion])
    pars = json.loads((V4 / "physical_parameters_frozen.json").read_text())["077"]
    k0, dc, bf = pars["physical"]
    delta = bf * np.log1p(cycle.v1_mm_s * cycle.t_h_s / dc) * np.exp(-cycle.branch_shift_mm / dc)
    lam = (cycle.A_N + delta) / k0
    correction = relaxation(s, cycle.A_N, delta, lam, dc)
    measured = f["force"][indices]
    full = f["physical"][indices]
    np.testing.assert_allclose(full[start-motion:], f["force"][rows] + correction, rtol=0, atol=1e-10)
    np.testing.assert_allclose(full[:start-motion+1], cycle.D_N, rtol=0, atol=1e-10)
    pre = np.full(start-motion, np.nan)
    return pd.DataFrame({
        "s_rec_mm": x, "time_s": f["time"][indices], "raw_row": indices, "measured_N": measured,
        "elastic_loading_only_N": np.r_[pre, cycle.D_N - cycle.A_N * np.exp(-s / pars["single"][0])],
        "complete_recovery_model_N": np.r_[pre, cycle.D_N - correction],
        "recovery_model_compensated_output_N": full,
        "recovery_model_correction_N": full - measured,
        "D_N": cycle.D_N, "reference_N": f["reference"][indices],
    })


def select_cycles(manifest, cache):
    table = pd.read_csv(BASE / "tables/table1_metrics_by_cycle.csv")
    table = table[(table.seed == -1) & (table.area == "S9_active")]
    table = table.pivot(index="cycle_id", columns="model_id", values="RMSE_N")
    recovery = pd.read_csv(BASE / "tables/recovery_metrics_by_cycle.csv")
    recovery = recovery[recovery.model_id == "double"].set_index("cycle_id")
    rows = []
    for cycle in manifest.itertuples(index=False):
        a = cycle_data(cycle, cache)
        raw = a.measured_N.to_numpy()
        full = a.recovery_model_compensated_output_N.to_numpy()
        elastic = raw + cycle.D_N - a.elastic_loading_only_N.to_numpy()
        elastic[a.raw_row.to_numpy() < int(cycle.onset_row)] = cycle.D_N
        ref = a.reference_N.to_numpy()
        rows.append({
            "cycle_id": cycle.cycle_id, "run_id": cycle.run_id, "samples_a": len(a),
            "full_to_raw_RMSE_N": float(np.sqrt(np.mean((full - raw)**2))),
            "elastic_to_raw_RMSE_N": float(np.sqrt(np.mean((elastic - raw)**2))),
            "full_to_reference_display_RMSE_N": float(np.sqrt(np.mean((full - ref)**2))),
            "S9_full_RMSE_N": table.loc[cycle.cycle_id, "double"],
            "S9_elastic_RMSE_N": table.loc[cycle.cycle_id, "single"],
            "S9_friction_RMSE_N": table.loc[cycle.cycle_id, "friction_only"],
            "measured_peak": recovery.loc[cycle.cycle_id, "measured_peak"],
            "predicted_peak": recovery.loc[cycle.cycle_id, "predicted_peak"],
            "activation_mm": cycle.branch_shift_mm, "A_N": cycle.A_N, "D_N": cycle.D_N,
        })
    screen = pd.DataFrame(rows)
    original = screen[screen.cycle_id == ORIGINAL_CYCLE].iloc[0]
    eligible = screen[(screen.cycle_id != ORIGINAL_CYCLE)
        & screen.measured_peak & screen.predicted_peak
        & (screen.full_to_raw_RMSE_N < original.full_to_raw_RMSE_N)
        & (screen.S9_full_RMSE_N < screen.S9_elastic_RMSE_N)
        & (screen.S9_full_RMSE_N < screen.S9_friction_RMSE_N)]
    selected = eligible.sort_values(["S9_full_RMSE_N", "full_to_raw_RMSE_N", "cycle_id"]).head(3).copy()
    assert len(selected) == 3 and selected.run_id.nunique() == 3
    selected["rank"] = np.arange(1, 4)
    # Keep the former typical cycle reproducible before screening new examples.
    original_a = cycle_data(manifest.loc[ORIGINAL_CYCLE], cache)
    saved_a = pd.read_csv(BASE / "source_data/figureA_a.csv")
    assert len(original_a) == len(saved_a) == 530
    np.testing.assert_allclose(original_a[saved_a.columns], saved_a, rtol=0, atol=1e-10, equal_nan=True)
    return selected, screen


def verify_raw(cycle, a):
    raw = pd.read_csv(cycle.raw_path, usecols=["axis1_pos_mm", "plc_time_us", "fn1_decoupled_delta_N"])
    rows = a.raw_row.to_numpy(int)
    np.testing.assert_array_equal(a.measured_N, raw.fn1_decoupled_delta_N.to_numpy()[rows])
    np.testing.assert_allclose(a.s_rec_mm, abs(raw.axis1_pos_mm.to_numpy()[rows] - raw.axis1_pos_mm.iloc[int(cycle.motion_onset_row)]), rtol=0, atol=1e-10)
    np.testing.assert_allclose(a.time_s, raw.plc_time_us.to_numpy()[rows] * 1e-6, rtol=0, atol=1e-10)


def output_name(cycle_id):
    return f"figureA_recovery_{cycle_id}_20261105"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(__file__).parent
    cache = {}
    manifest = read_manifest()
    selected, screen = select_cycles(manifest, cache)
    summary_path = out / "figureA_recovery_candidates_20261105.csv"
    targets = [out / (output_name(cid) + ext) for cid in selected.cycle_id for ext in (".pdf", ".png")]
    for path in targets + [summary_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite: {path}")
    for cid in selected.cycle_id:
        cycle = manifest.loc[cid]
        data = cycle_data(cycle, cache)
        verify_raw(cycle, data)
        figure, report = build_figure(cycle, data)
        save_figure(figure, out / output_name(cid))
        plt.close(figure)
    with summary_path.open("x", encoding="utf-8-sig", newline="") as handle:
        selected.to_csv(handle, index=False)
    print(selected.to_string(index=False))
