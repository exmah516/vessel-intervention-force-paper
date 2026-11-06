from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties

SKILL = Path.home() / '.codex' / 'skills' / 'nature-figure' / 'scripts'
if SKILL.exists() and str(SKILL) not in sys.path:
    sys.path.insert(0, str(SKILL))
from audit_panel_alignment import require_matplotlib_panel_alignment

RECORD_DIR = Path(r'D:\Work_files\Vessel intervention Robot\260316\dual_clamp_experiment\x64\Debug\records\20261031_083641_交接等待时间0s（与第一组位置相同）')
OUT_STEM = Path(__file__).resolve().with_suffix('')
FONT_CN = Path(r'C:\Windows\Fonts\simsun.ttc')
FONT_EN = Path(r'C:\Windows\Fonts\times.ttf')
CN = FontProperties(fname=str(FONT_CN), size=9)
EN = FontProperties(fname=str(FONT_EN), size=9, math_fontfamily='custom')
START_S = 13.754
END_S = 19.222
PHASES = [
    (13.754, 14.972, 'I 递送与停止（S1～S2）', '#E6F1E5'),
    (14.972, 16.474, 'II 卸载交接（S3～S4）', '#FFF0D5'),
    (16.474, 17.692, 'III 空载回程（S5～S6）', '#F9E1DE'),
    (17.692, 19.222, 'IV 重新承载与递送（S7～S10）', '#E2ECF6'),
]


def opaque_color(color: str, alpha: float) -> tuple[float, float, float]:
    return tuple(alpha * value + (1.0 - alpha) for value in mpl.colors.to_rgb(color))


def main() -> None:
    outputs = [OUT_STEM.with_suffix(ext) for ext in
        ('.pdf', '.png', '.json', '.alignment.json', '.alignment.svg', '.collision-audit.json', '.collision-audit.pdf')]
    outputs.append(OUT_STEM.with_name(OUT_STEM.name + '_source.csv'))
    existing = [str(path) for path in outputs if path.exists()]
    if existing:
        raise FileExistsError('Refusing to overwrite: ' + ', '.join(existing))
    if not FONT_CN.exists() or not FONT_EN.exists():
        raise FileNotFoundError('需要系统宋体与 Times New Roman 字体文件。')

    metadata = json.loads((RECORD_DIR / 'experiment.json').read_text(encoding='utf-8'))
    source = RECORD_DIR / 'samples_1khz.csv'
    df = pd.read_csv(source)
    source_sample_count = len(df)
    absolute_time = df['plc_time_us'].to_numpy(dtype=float) / 1e6
    window = (absolute_time >= START_S) & (absolute_time <= END_S)
    df = df.loc[window].copy().reset_index(drop=True)
    absolute_time = absolute_time[window]
    metadata['source_sample_count'] = source_sample_count
    metadata['selected_window_samples'] = len(df)
    metadata['samples_outside_selected_window'] = source_sample_count - len(df)
    assert len(df) == 5469 and np.isclose(absolute_time[0], START_S) and np.isclose(absolute_time[-1], END_S)

    slopes = metadata['sensor_slopes_N_per_count']
    fn1 = (df['fn1_raw'].to_numpy(dtype=float) - float(metadata['fn1_zero'])) * float(slopes['fn1'])
    ft1 = (df['ft1_raw'].to_numpy(dtype=float) - float(metadata['ft1_zero'])) * float(slopes['ft1'])
    axial = fn1 * float(metadata['installation_axial_gain'])
    torque = ft1 * float(metadata['installation_torque_gain_Nmm_per_N'])
    decoupling = np.asarray(metadata['decoupling_matrix'], dtype=float)
    force = decoupling[0, 0] * axial + decoupling[0, 1] * torque
    assert np.allclose(force, df['fn1_decoupled_delta_N'].to_numpy(dtype=float), atol=1e-10)

    relative_time = absolute_time - START_S
    position = df['axis1_pos_mm'].to_numpy(dtype=float)
    forward_travel = position[0] - position
    force_median = pd.Series(force).rolling(window=21, center=True, min_periods=1).median().to_numpy()
    phase = np.select([(absolute_time >= start) & ((absolute_time < end) if end < END_S else (absolute_time <= end))
        for start, end, _, _ in PHASES], [label for _, _, label, _ in PHASES], default='')
    assert not np.any(phase == '')

    # Recorded command edges and phase labels anchor the four color blocks.
    expected_edges = [(14.972, 'phase4-to-phase5'), (16.474, 'phase5-to-phase6'),
        (17.692, 'phase6-to-phase7'), (18.005, 'next-cycle-forward-start')]
    event_rows = []
    for event_time, label in expected_edges:
        row = int(np.argmin(np.abs(absolute_time - event_time)))
        assert abs(absolute_time[row] - event_time) <= .001
        event_rows.append({'event': label, 'time_s': float(absolute_time[row]), 'row': int(df.index[row])})
    expected_phase_edges = [(13.754, 4, 4), (14.972, 4, 5), (16.474, 4, 6),
        (17.692, 4, 7), (18.005, 5, 4), (19.222, 5, 4)]
    for event_time, cycle, phase_code in expected_phase_edges:
        row = int(np.argmin(np.abs(absolute_time - event_time)))
        assert abs(absolute_time[row] - event_time) <= .001
        assert int(df['cycle_index'].iloc[row]) == cycle and int(df['phase'].iloc[row]) == phase_code
    command_edges = [(15.473, 'cylinder1_cmd', 550, 5),
        (15.973, 'cylinder2_cmd', 1000, 5), (17.693, 'cylinder2_cmd', 5, 1000),
        (17.743, 'cylinder1_cmd', 5, 550)]
    for event_time, column, before, after in command_edges:
        row = int(np.argmin(np.abs(absolute_time - event_time)))
        assert abs(absolute_time[row] - event_time) <= .001
        assert row > 0 and int(df[column].iloc[row - 1]) == before and int(df[column].iloc[row]) == after
        event_rows.append({'event': f'{column}:{before}->{after}',
            'time_s': float(absolute_time[row]), 'row': int(df.index[row])})
    c5 = df[(df['cycle_index'] == 5) & (df['phase'] == 4)]
    assert len(c5) == 1218 and np.isclose(c5['plc_time_us'].iloc[0] / 1e6, 18.005)
    reclamp_time = float(absolute_time[np.argmin(np.abs(absolute_time - 17.693))])
    next_push_time = float(absolute_time[np.argmin(np.abs(absolute_time - 18.005))])
    reclamp_wait_s = next_push_time - reclamp_time
    assert reclamp_wait_s < .4
    traces = []
    for cycle_index in (4, 5):
        group = df[(df['cycle_index'] == cycle_index) & (df['phase'] == 4)]
        y = group['fn1_decoupled_delta_N'].to_numpy(dtype=float)
        t = group['plc_time_us'].to_numpy(dtype=float) / 1e6
        peak = int(np.argmax(y))
        tail = y[t >= t[-1] - .2]
        traces.append({'cycle': int(cycle_index), 'start_s': float(t[0]), 'end_s': float(t[-1]),
            'start_force_N': float(y[0]), 'peak_force_N': float(y[peak]),
            'peak_time_from_start_s': float(t[peak] - t[0]),
            'tail_median_last_0p2s_N': float(np.median(tail)),
            'tail_iqr_last_0p2s_N': [float(np.quantile(tail, .25)), float(np.quantile(tail, .75))]})
    tail_difference_N = abs(traces[0]['tail_median_last_0p2s_N'] - traces[1]['tail_median_last_0p2s_N'])
    assert tail_difference_N < .05

    data = pd.DataFrame({'record_time_s': absolute_time, 'relative_time_s': relative_time,
        'axial_force_reconstructed_N': force, 'axial_force_21ms_median_N': force_median,
        'forward_travel_from_window_start_mm': forward_travel, 'cycle_index': df['cycle_index'].to_numpy(),
        'phase_code': df['phase'].to_numpy(), 'phase_color_block': phase})
    data.to_csv(OUT_STEM.with_name(OUT_STEM.name + '_source.csv'), index=False, encoding='utf-8-sig')

    mpl.rcParams.update({'font.family': ['Times New Roman'], 'font.size': 9,
        'axes.labelsize': 9, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
        'legend.fontsize': 9, 'axes.linewidth': .7, 'axes.spines.top': False,
        'axes.spines.right': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'ps.fonttype': 42, 'mathtext.fontset': 'custom', 'mathtext.rm': 'Times New Roman',
        'mathtext.it': 'Times New Roman:italic', 'mathtext.bf': 'Times New Roman:bold',
        'mathtext.fallback': None, 'savefig.facecolor': 'white', 'path.simplify': False})
    fig, (ax_force, ax_position) = plt.subplots(2, 1, figsize=(7.60 / 2.54, 3.0 / 2.54),
        sharex=True, gridspec_kw={'height_ratios': [1.1, 1.0], 'hspace': .18})
    fig.subplots_adjust(left=.13, right=.985, top=.94, bottom=.26)
    for start, end, _, color in PHASES:
        for ax in (ax_force, ax_position):
            ax.axvspan(start - START_S, end - START_S,
                color=opaque_color(color, .72), lw=0, zorder=0)
    ax_force.plot(relative_time, force / 2.12, color=opaque_color('#8A929B', .72), lw=.48, zorder=2)
    ax_force.plot(relative_time, force_median / 2.12, color='#183A52', lw=.95, zorder=3)
    ax_force.set_ylabel(r'$F$ₓ / N', fontproperties=EN)
    ax_force.set_ylim(-.25, 2.15)
    ax_force.set_yticks([0, 1, 2])
    ax_force.grid(axis='y', color=opaque_color('#C9CED4', .65), lw=.45, zorder=1)
    ax_force.tick_params(axis='x', labelbottom=False, length=2.2, width=.6, pad=2)
    ax_force.tick_params(axis='y', length=2.2, width=.6, pad=1.5)
    ax_position.plot(relative_time, forward_travel, color='#4F6272', lw=.85, zorder=2)
    ax_position.set_ylabel(r'$x_m$ / mm', fontproperties=EN)
    ax_position.set_ylim(-1, 21)
    ax_position.set_yticks([0, 10, 20])
    ax_position.grid(axis='y', color=opaque_color('#C9CED4', .65), lw=.45, zorder=1)
    ax_position.set_xlabel(r'$t$ / s', fontproperties=EN, labelpad=1.5)
    ax_position.set_xlim(0, END_S - START_S + .001)
    ax_position.set_xticks(np.arange(0, 6.51, 1.0))
    ax_position.tick_params(axis='x', length=2.2, width=.6, pad=1.5)
    ax_position.tick_params(axis='y', length=2.2, width=.6, pad=1.5)
    for ax in (ax_force, ax_position):
        ax.yaxis.set_label_coords(-.08, .5, transform=ax.transAxes)
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig, json_out=OUT_STEM.with_suffix('.alignment.json'),
        overlay_svg=OUT_STEM.with_suffix('.alignment.svg'), axes=(ax_force, ax_position),
        panel_ids=['force', 'position'], column_groups=[['force', 'position']],
        tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=True)
    fig.savefig(OUT_STEM.with_suffix('.pdf'))
    fig.savefig(OUT_STEM.with_suffix('.png'), dpi=600)
    plt.close(fig)

    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    report = {'record': metadata['directory_name'], 'cycles': [4, 5], 'samples': len(data),
        'source_sha256': digest, 'phase_boundaries_absolute_s': [x[0] for x in PHASES] + [PHASES[-1][1]],
        'main_reclamp_to_next_forward_start_s': reclamp_wait_s,
        'last_0p2s_force_median_difference_N': tail_difference_N,
        'event_rows': event_rows, 'cycle_force_features': traces,
        'plot_style': {'width_cm': 7.6, 'height_cm': 3.0, 'font_pt': 9,
            'force_display_scale': 'existing figure1 script: reconstructed force / 2.12',
            'raw_and_existing_21ms_median_traces': True},
        'source_sample_count': source_sample_count, 'selected_window_samples': len(data),
        'samples_outside_selected_window': source_sample_count - len(data),
        'new_filtering_or_scaling_of_source_data': False}
    OUT_STEM.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    auditor = SKILL / 'audit_figure_collisions.py'
    if auditor.exists():
        subprocess.run([sys.executable, str(auditor), str(OUT_STEM.with_suffix('.pdf')),
            '--json-out', str(OUT_STEM.with_suffix('.collision-audit.json')),
            '--overlay-pdf', str(OUT_STEM.with_suffix('.collision-audit.pdf'))], check=False)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
