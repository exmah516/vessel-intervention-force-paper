"""Re-export Figure D with the requested legend/annotation cleanup only."""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

SOURCE = Path(r"D:\Work_files\Vessel intervention Robot\paper\outputs\paper_selected_results_20261104\qa\figureD_76mm_9pt")
S9_COLOR = "#E5EFF5"
TAPER_COLOR = "#D8ECE7"


def build():
    font_manager.findfont("SimSun", fallback_to_default=False)
    font_manager.findfont("Times New Roman", fallback_to_default=False)
    plt.rcParams.update({
        "font.family": ["Times New Roman", "SimSun"], "font.size": 9,
        "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
        "legend.fontsize": 9, "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none", "path.simplify": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": .7, "xtick.major.size": 3,
        "ytick.major.size": 3, "lines.linewidth": .8,
    })
    data = pd.read_csv(SOURCE / "selected_three_source.csv")
    selection = json.loads((SOURCE / "selection.json").read_text(encoding="utf-8"))
    phases = selection["phases"]
    assert len(data) == 936 and len(phases) == 3
    sec = data.relative_time_s.to_numpy()
    raw = data.corrected_measurement_N.to_numpy()
    method = data.frozen_physical_network_output_N.to_numpy()
    assert np.all(np.diff(sec) > 0) and np.isfinite(raw).all() and np.isfinite(method).all()

    fig, ax = plt.subplots(figsize=(76 / 25.4, 55 / 25.4))
    fig.subplots_adjust(left=.19, right=.97, bottom=.21, top=.69)
    for phase in phases:
        ax.axvspan(phase["j"], phase["k"], color=S9_COLOR, zorder=0)
        ax.axvspan(phase["k"], min(phase["k"] + .1, phase["end"]), color=TAPER_COLOR, zorder=0)
    for phase in phases[1:]:
        ax.axvline(phase["a"], color="#7C858B", linestyle=(0, (2, 2)), linewidth=.55)
    ax.plot(sec, raw, color="#676767", linestyle="-", linewidth=.65)
    ax.plot(sec, method, color="#CC79A7", linewidth=1.05)
    ax.set_ylabel("轴向载荷 / N")
    ax.set_xlabel("相对时间 / s")
    ax.grid(axis="y", alpha=.15, linewidth=.5)
    handles = [
        Line2D([], [], color="#676767", ls="-", lw=.65, label="原始数据"),
        Line2D([], [], color="#CC79A7", lw=1.05, label="本文方法"),
        Patch(facecolor=S9_COLOR, label="S9"),
    ]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.53, .92),
               ncol=3, frameon=False, handlelength=1.2,
               columnspacing=.65, handletextpad=.35)
    fig.canvas.draw()
    assert len(ax.lines) == 4  # two traces and the two cycle separators
    assert all(text.get_text() not in {"C01", "C02", "C03"} for text in ax.texts)
    assert len(ax.patches) == 6  # S9 and withdrawal-taper shading for three cycles
    return fig, {"samples": len(data), "cycles": len(phases), "cycle_ids": selection["selected"]["cycle_ids"],
                 "removed_period_hold_lines": True, "legend": ["原始数据", "本文方法", "S9"],
                 "size_mm": [76, 55], "font_pt": 9}


def save(fig, prefix):
    for ext in (".pdf", ".png"):
        path = prefix.with_suffix(ext)
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite {path}")
    for ext in (".pdf", ".png"):
        path = prefix.with_suffix(ext)
        with path.open("xb") as stream:
            fig.savefig(stream, format=ext[1:], dpi=600)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    prefix = Path(__file__).with_suffix("")
    if any(prefix.with_suffix(ext).exists() for ext in (".pdf", ".png")):
        raise FileExistsError("Refusing to overwrite an existing figure")
    fig, info = build()
    save(fig, prefix)
    plt.close(fig)
    print(json.dumps(info, ensure_ascii=False, indent=2))
