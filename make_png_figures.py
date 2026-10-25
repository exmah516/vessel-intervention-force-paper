import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

out_dir = r'D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\JQR_LaTeX_Template-0507'

figures = [
    (
        "fig1.png",
        "图 1  往复夹持递送S1～S10工作时序与物理相演变\nFig.1 Timing of S1–S10 stages and evolution of physical phases during reciprocating clamping delivery",
        "【拟配图内容】\n1. S1～S10 十个阶段时序与四个物理相划分（稳态递送、卸载交接、空载回程、重加载交接与稳态恢复）；\n2. 主爪与副爪开合动作状态、滑台位移曲线及同步主爪／副爪／参考载荷演变；\n3. 重点突出 S3 第一次双爪共持、S7 第二次双爪共持、S8 副爪释放与被动分配、S9 恢复推进与弹性重加载爬升。"
    ),
    (
        "fig2.png",
        "图 2  测力支路受力分析及多阶段串联变形传力演变示意图\nFig.2 Force analysis of sensing branch and schematic of multi-stage series deformation and load transfer evolution",
        "【图2占位说明】\n(a) 近端二自由度测力支路与内侧浮动传力组件隔离体受力分析图，标明远端阻力反作用力、浮动组件惯性力 ms*aM、旋转支路摩擦阻尼力矩及传感器敏感轴正方向；\n(b) 主副夹爪多级串联刚度等效模型，以及 S1（主爪独立稳态承载）、S8（副爪松开后导丝微回缩与主爪被动承接部分载荷）、S9（主爪恢复推进与旋转时的复合弹性变形重建）三个典型阶段的变形与传力演变示意图。"
    ),
    (
        "fig3.png",
        "图 3  物理基线与GRU时序残差融合补偿框图\nFig.3 Compensation framework combining the physical baseline and GRU temporal residual network",
        "【图3占位说明】\n物理基线与 GRU 残差网络融合补偿框图。左侧输入主爪运动状态与原始测力，上方支路通过运动干扰扣除与二维耦合重加载公式计算物理基线 w_out,k^(0)；下方支路将物理基线、换手前锁存载荷 D_9,k、含相对恢复行程的运动状态 q_M,k、夹爪时序及干扰估计组成短时窗口，输入 GRU 预测残差 r_k。\n物理基线减去残差后，经 S4～S8 锁存与 S9 边界平滑输出最终反馈 w_fb,k。标注稳态基准的更新、锁存及 S8 末测量初始化重加载项的位置；以虚线表示离线训练时由连续递送参考构造残差标签，S9 参考来自配对不换手试次。"
    ),
    (
        "fig4.png",
        "图 4  纯轴向与复合递送工况下各方法的连续力反馈重构效果对比\nFig.4 Comparison of continuous force feedback reconstruction performance among methods under axial and composite delivery conditions",
        "【拟配图内容】\n1. 纯轴向往复递送工况与推进—旋转复合递送工况时间响应曲线；\n2. 原始测量（Raw）、传统低通滤波（LPF）、仅物理基线补偿（Physics Baseline）与物理融合 GRU 残差补偿（Physics + GRU）对比；\n3. 同轴配对不换手试次提供的连续递送参考载荷（Continuous Reference）基准对照；\n4. 轴向力、测量扭矩、换向冲击及 S9 重加载恢复阶段局部放大视图。"
    ),
    (
        "fig5.png",
        "图 5  稳态递送与重加载阶段未训练阻力突变扰动下的动态响应与保留效果\nFig.5 Dynamic response and preservation performance under untrained resistance disturbance injection during steady delivery and reloading stages",
        "【图5占位说明】\n(a) 同轴台架 S1 稳态递送阶段的未训练阻力突变响应，绘制参考载荷及各方法输出；\n(b) 同轴台架 S9 初始推进阶段的响应，分别绘制实际承载参考、配对不换手连续递送参考和各方法输出，并用对应无扰动试次提取突变增量，标注施加位置、峰值增量、保留率和响应延迟；\n(c) 血管模型受压递送中 S1 与 S9 局部阻力突变的原始及补偿波形，标注施加时刻。各子图明确区分两套台架，定量保留率和延迟来自同轴配对试次。"
    ),
    (
        "fig6.png",
        "图 6  消融实验与多工况泛化性能综合评估\nFig.6 Comprehensive evaluation of ablation studies and multi-condition generalization performance",
        "【图6占位说明】\n(a) Physics + GRU、w/o Reloading Term 与 Pure GRU 的 S9 连续反馈重构曲线，绘制配对不换手参考及局部误差，标注共同的锁存和平滑设置；\n(b) 分组比较 S1/S2/S10 的测量 MAE、RMSE 和 S9 的连续反馈重构 MAE、RMSE、恢复时间；\n(c) 按器械类型、运动速度与载荷条件列出独立测试结果，并报告批大小为 1 的在线推理耗时。两组消融均保留稳态载荷记忆和恢复行程，使用相同连续递送目标及配对数据划分；移除重加载项后重新构造标签并训练，Pure GRU 直接预测连续递送载荷。"
    ),
]

for filename, title, desc in figures:
    fig, ax = plt.subplots(figsize=(8.5, 4.4), dpi=220)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Outer rectangle
    rect = patches.FancyBboxPatch((0.2, 0.2), 9.6, 4.6,
                                  boxstyle="round,pad=0.2",
                                  linewidth=1.8,
                                  edgecolor="#1f77b4",
                                  facecolor="#f6f9fc",
                                  linestyle="--")
    ax.add_patch(rect)
    
    # Header rectangle
    header_rect = patches.FancyBboxPatch((0.5, 3.7), 9.0, 0.9,
                                         boxstyle="round,pad=0.1",
                                         linewidth=1,
                                         edgecolor="#aec7e8",
                                         facecolor="#e1edf8")
    ax.add_patch(header_rect)
    
    ax.text(5.0, 4.15, title, fontsize=10.5, fontweight='bold',
            ha='center', va='center', color="#0f3b6c", multialignment='center')
    
    ax.text(5.0, 2.1, desc, fontsize=9.2,
            ha='center', va='center', color="#222222", multialignment='left',
            linespacing=1.55)
    
    ax.text(5.0, 0.45, "[ 《机器人》论文投稿插图占位符 - 请于录用待发表阶段替换为正式矢量图 ]",
            fontsize=8.5, style='italic', ha='center', va='center', color="#7f7f7f")
    
    plt.tight_layout()
    out_path = os.path.join(out_dir, filename)
    plt.savefig(out_path, format='png', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")
