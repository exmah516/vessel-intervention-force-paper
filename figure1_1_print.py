from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

# Ensure local audit scripts in ~/.codex can be imported
SKILL = Path.home() / ".codex" / "skills" / "nature-figure" / "scripts"
if SKILL.exists() and str(SKILL) not in sys.path:
    sys.path.insert(0, str(SKILL))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch

from audit_panel_alignment import require_matplotlib_panel_alignment


RECORD_DIR = Path(
    r"D:\Work_files\Vessel intervention Robot\260316\dual_clamp_experiment\x64\Debug\records\20261024_223400_导管鞘和血管模型中的正常导管-纯轴向往复"
)
SCRIPT_DIR = Path(__file__).resolve().parent
OUT_STEM = SCRIPT_DIR / "figure1_1_print"

FONT_CN = Path(r"C:\Windows\Fonts\simsun.ttc")
FONT_EN = Path(r"C:\Windows\Fonts\times.ttf")
CN = FontProperties(fname=str(FONT_CN), size=9)
EN = FontProperties(fname=str(FONT_EN), size=9)

PHASES = [
    (1.001, 2.313, "I 稳态递送", "#E6F1E5"),
    (2.313, 4.463, "II 换手与回退", "#FFF0D5"),
    (4.463, 4.840, "III 重加载", "#F9E1DE"),
    (4.840, 5.741, "IV 恢复后递送", "#E2ECF6"),
]


def load_and_reconstruct() -> tuple[pd.DataFrame, dict[str, float], str]:
    metadata = json.loads((RECORD_DIR / "experiment.json").read_text(encoding="utf-8"))
    source = RECORD_DIR / "samples_1khz.csv"
    df = pd.read_csv(source)
    t_s = df["plc_time_us"].to_numpy(dtype=float) / 1e6
    window = (t_s >= 1.001) & (t_s <= 5.741)
    df = df.loc[window].copy().reset_index(drop=True)
    t_s = t_s[window]

    slopes = metadata["sensor_slopes_N_per_count"]
    fn1 = (df["fn1_raw"].to_numpy(dtype=float) - float(metadata["fn1_zero"])) * float(slopes["fn1"])
    ft1 = (df["ft1_raw"].to_numpy(dtype=float) - float(metadata["ft1_zero"])) * float(slopes["ft1"])
    axial_pre = fn1 * float(metadata["installation_axial_gain"])
    torque_pre = ft1 * float(metadata["installation_torque_gain_Nmm_per_N"])
    decoupling = np.asarray(metadata["decoupling_matrix"], dtype=float)
    measured_force = decoupling[0, 0] * axial_pre + decoupling[0, 1] * torque_pre

    # Position sign is reversed in the recorded encoder convention: forward travel is positive here.
    pos = df["axis1_pos_mm"].to_numpy(dtype=float)
    forward_travel = pos[0] - pos
    main_closed = df["cylinder2_cmd"].to_numpy(dtype=float) >= 300
    auxiliary_closed = df["cylinder1_cmd"].to_numpy(dtype=float) >= 200
    time_s = t_s - 1.001

    data = pd.DataFrame(
        {
            "record_time_s": t_s,
            "relative_time_s": time_s,
            "axial_force_reconstructed_N": measured_force,
            "forward_travel_from_window_start_mm": forward_travel,
            "main_clamp_command_closed": main_closed.astype(int),
            "auxiliary_clamp_command_closed": auxiliary_closed.astype(int),
            "phase": np.select(
                [
                    (t_s >= start) & (t_s < end)
                    for start, end, _, _ in PHASES
                ],
                [label for _, _, label, _ in PHASES],
                default="",
            ),
        }
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    return data, metadata, digest


def main() -> None:
    if not FONT_CN.exists() or not FONT_EN.exists():
        raise FileNotFoundError("需要系统宋体与 Times New Roman 字体文件。")

    data, metadata, digest = load_and_reconstruct()
    time_s = data["relative_time_s"].to_numpy()
    record_time_s = data["record_time_s"].to_numpy()
    force = data["axial_force_reconstructed_N"].to_numpy()
    travel = data["forward_travel_from_window_start_mm"].to_numpy()

    # A centered 21 ms median line reduces sample-level jitter; the reconstructed samples remain visible underneath.
    force_median = pd.Series(force).rolling(window=21, center=True, min_periods=1).median().to_numpy()
    data["axial_force_21ms_median_N"] = force_median
    data.to_csv(OUT_STEM.with_name("figure1_1_source.csv"), index=False, encoding="utf-8-sig")

    # Scale the top plot's force values by dividing by 2.12 before plotting
    force_plot = force / 2.12
    force_median_plot = force_median / 2.12

    mpl.rcParams.update(
        {
            "font.family": ["Times New Roman", "Arial"],
            "font.size": 9,
            "axes.labelsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "axes.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "mathtext.fontset": "stix",
            "savefig.facecolor": "white",
        }
    )

    # Figure width 7.62cm (3.0 in), height compressed to ~3.0cm (1.181 in)
    fig, (ax_force, ax_position) = plt.subplots(
        2,
        1,
        figsize=(7.62 / 2.54, 3.0 / 2.54),
        sharex=True,
        gridspec_kw={"height_ratios": [1.1, 1.0], "hspace": 0.18},
    )
    # Narrow the left margin as much as possible while preventing clipping
    fig.subplots_adjust(left=0.13, right=0.985, top=0.94, bottom=0.26)
    axes = (ax_force, ax_position)

    for start, end, label, color in PHASES:
        for ax in axes:
            ax.axvspan(start - 1.001, end - 1.001, color=color, alpha=0.72, lw=0, zorder=0)

    # Top subplot: F_x
    ax_force.plot(time_s, force_plot, color="#8A929B", lw=0.48, alpha=0.72, zorder=2)
    ax_force.plot(time_s, force_median_plot, color="#183A52", lw=0.95, zorder=3)
    ax_force.set_ylabel(r"$F$ₓ / N", fontproperties=EN)
    ax_force.set_ylim(-0.25, 2.15)
    ax_force.set_yticks([0, 1, 2])
    ax_force.grid(axis="y", color="#C9CED4", lw=0.45, alpha=0.65, zorder=1)
    ax_force.tick_params(axis="x", labelbottom=False, length=2.2, width=0.6, pad=2)
    ax_force.tick_params(axis="y", length=2.2, width=0.6, pad=1.5)

    # Middle subplot (now bottom subplot): s_m with horizontal axis annotations from former clamp panel
    ax_position.plot(time_s, travel, color="#4F6272", lw=0.85, zorder=2)
    ax_position.set_ylabel(r"$s$ₘ / mm", fontproperties=EN)
    ax_position.set_ylim(-1, 21)
    ax_position.set_yticks([0, 10, 20])
    ax_position.grid(axis="y", color="#C9CED4", lw=0.45, alpha=0.65, zorder=1)
    ax_position.set_xlabel(r"$t$ / s", fontproperties=EN, labelpad=1.5)
    ax_position.set_xlim(0, 5.741 - 1.001)
    ax_position.set_xticks(np.arange(0, 4.751, 0.5))
    ax_position.tick_params(axis="x", length=2.2, width=0.6, pad=1.5)
    ax_position.tick_params(axis="y", length=2.2, width=0.6, pad=1.5)

    # Align y-labels and adjust s distance to y-axis according to F_x/N
    label_x_axis = -0.08
    ax_force.yaxis.set_label_coords(label_x_axis, 0.5, transform=ax_force.transAxes)
    ax_position.yaxis.set_label_coords(label_x_axis, 0.5, transform=ax_position.transAxes)

    fig.canvas.draw()
    require_matplotlib_panel_alignment(
        fig,
        json_out=OUT_STEM.with_suffix(".alignment.json"),
        overlay_svg=OUT_STEM.with_suffix(".alignment.svg"),
        axes=axes,
        panel_ids=["force", "position"],
        column_groups=[["force", "position"]],
        tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,
        strict=True,
    )

    fig.savefig(OUT_STEM.with_suffix(".pdf"))
    fig.savefig(OUT_STEM.with_suffix(".svg"))
    fig.savefig(OUT_STEM.with_suffix(".png"), dpi=600)
    fig.savefig(OUT_STEM.with_suffix(".tif"), dpi=600)
    plt.close(fig)

    auditor = SKILL / "audit_figure_collisions.py"
    if auditor.exists():
        subprocess.run(
            [
                sys.executable,
                str(auditor),
                str(OUT_STEM.with_suffix(".pdf")),
                "--json-out",
                str(OUT_STEM.with_suffix(".collision-audit.json")),
                "--overlay-pdf",
                str(OUT_STEM.with_suffix(".collision-audit.pdf")),
            ],
            check=False,
        )

    notes = [
        "图1数据说明",
        "核心信息：该真实往复周期包含稳态递送、交接与回退、重加载、恢复后递送四段；原始重构轴向测力在重加载时回升。",
        "记录：2026-10-24 正常导管、导管鞘与血管模型、纯轴向往复。",
        "时间范围：记录时刻 1.001–5.741 s；阶段边界为 2.313、4.463、4.840 s。S9 边界由实际速度起动和累计5 mm实际行程确定。",
        "测力：由原始计数、文件零点、传感器斜率、安装增益和既有解耦矩阵重构；绘图时按要求将轴向测力纵坐标数值除以2.12显示。浅灰线为重构采样，深蓝线为居中21 ms中值线，减弱显示抖动。",
        "位移：编码器位置相对窗口起点换算为前进为正的位移。最下方夹爪状态子图已移除，时间轴移至位移图。",
        "排版：图宽保持7.62 cm，高度压缩至约3.0 cm；左侧空白边距缩窄，纵坐标标题左对齐并统一距纵坐标轴的距离。",
        "数据处理：没有修改S10趋势或将下降段替换成平台；图中小幅波动/下降均保留。没有删去窗口内采样点。",
        f"原始采样SHA-256：{digest}",
        f"解耦矩阵：{metadata['decoupling_matrix']}",
    ]
    OUT_STEM.with_name("figure1_1_qa.txt").write_text("\n".join(notes), encoding="utf-8")
    print(f"Saved: {OUT_STEM.with_suffix('.pdf')}")
    print(f"Source samples: {len(data)}; raw SHA-256: {digest}")
    print("S10 measured variation is preserved; no trend was artificially flattened.")


if __name__ == "__main__":
    main()
