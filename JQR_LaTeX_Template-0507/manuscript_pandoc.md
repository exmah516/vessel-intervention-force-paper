
第xx 卷第x 期 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 机器人 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Vol.xx, No.x  
2026 年10 月 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ROBOT &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Oct., 2026  
DOI：10.13973/j.cnki.robot.240001  
CSTR：32165.14.robot.240001  

# 面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制

隋凯丞^1,2,3^，郑力铭^1,2,3^，林 鹏^1,2^，胡琨元^1,2\*^，刘 浩^1,2\*^

（1. 中国科学院沈阳自动化研究所 机器人学国家重点实验室，辽宁 沈阳 110016）

（2. 辽宁省微创手术机器人重点实验室，辽宁 沈阳 110016）

（3. 中国科学院大学，北京 100049）

（4. 中国人民解放军北部战区总医院，辽宁 沈阳 110016）

**摘 要**：【目的】针对往复夹持式血管介入机器人中机构运动与夹爪切换引起的附加测力波动，研究力反馈扰动建模与残差补偿方法，重构相同递送条件下不发生夹爪换手时的连续力反馈。【方法】将主副夹爪的递送、交接、回程和重夹持过程划分为S1～S10十个阶段，建立浮动传力组件的惯性干扰模型与多级串联刚度模型；采用轴向与周向耦合的等效恢复行程，计算重加载实际承载与连续递送目标之间的补偿量，并将物理基线输出、换手前稳态载荷、相对运动与夹爪时序输入门控循环单元（GRU）网络，估计物理基线与连续递送参考之间的残差；通过交接期数值锁存与边界平滑输出反馈力和扭矩。【结果】在无血管模型的双单元同轴对拉、对扭台架上，以不换手递送试次作为连续载荷参考，评价稳态与重加载阶段的反馈重构误差、完整交接重加载周期的输出波动及S1/S9阶段的未训练阻力突变响应，并在介入血管模型中验证受压推进与旋转递送的反馈波形。重构误差、最大波动及扰动响应结果为[待补]。【结论】物理模型与GRU残差补偿相结合，为往复夹持递送中的连续力反馈重构提供了方法。

**关键词**：导丝；介入机器人；夹持机构；接触力学；扭矩传递；力反馈；GRU神经网络

# Disturbance Modeling and Residual Suppression of Force Feedback for Vascular Intervention Robot in Reciprocating Clamping Delivery

SUI Kaicheng^1,2,3^, LIN Peng^1,2^, WANG Chongyang^1,2^, ZHANG Yuhang^1,2^, PAN Pengyu^4^, LIU Hao^1,2\*^

(1. State Key Laboratory of Robotics, Shenyang Institute of Automation, Chinese Academy of Sciences, Shenyang 110016, China)

(2. Key Laboratory of Minimally Invasive Surgical Robot, Liaoning Province, Shenyang 110016, China)

(3. University of Chinese Academy of Sciences, Beijing 100049, China)

(4. Northern Theater Command General Hospital, Shenyang 110016, China)

**Abstract**: [Objective] A disturbance model and residual compensation method are developed to reconstruct the continuous force feedback expected without gripper handover under matched delivery conditions in a reciprocating clamping vascular intervention robot. [Methods] The delivery, handover, return, and reclamping cycle is divided into ten stages (S1--S10). An inertial disturbance model of the floating load transmission assembly and a series stiffness model are established. A coupled axial-rotational recovery travel is used to calculate the compensation between the actual reloading load and the continuous-delivery target. The physical baseline, stored steady load before handover, relative motion, and gripper timing are supplied to a gated recurrent unit (GRU) network to estimate the residual relative to a continuous-delivery reference. Numerical holding during handover and boundary smoothing are applied to the force and torque feedback. [Results] Uninterrupted delivery trials on a coaxial tensile and torsional test rig provide the continuous-load reference for evaluating feedback reconstruction errors during steady delivery and reloading, output fluctuations over the complete handover and reloading cycle, and responses to untrained resistance changes in S1 and S9. Feedback waveforms are also examined during compressive delivery and rotation in a vascular phantom. Reconstruction errors, maximum fluctuations, and disturbance response results are [to be added]. [Conclusions] Combining the physical model with GRU residual compensation provides a method for reconstructing continuous force feedback during reciprocating clamping delivery.

**Keywords**: guidewire; intervention robot; clamping mechanism; contact mechanics; torque transmission; force feedback; gated recurrent unit (GRU)

**基金项目**：国家自然科学基金联合基金项目（U23A20338）；国家重点研发计划智能机器人重点专项（2022YFB4703500）；辽宁省自然科学基金优青项目（2023-MS-021）．

**通信作者**：刘浩，Email: liuhao@sia.cn

**收稿／录用／修回**：2026-10-21/2026-10-21/2026-10-21

---

血管内介入治疗是实现心血管及脑血管疾病微创诊治的重要手段。在传统手术中，医师需在X射线透视引导下手动推进并旋转导丝与导管，这一过程不仅高度依赖术者的精准操作技巧与临床经验，还使术者长期暴露于电离辐射并承受沉重的铅衣负担^\[1\]^。血管介入机器人通过主从遥操作模式驱动柔性器械完成递送与旋转，可将术者与辐射源物理隔离，并提供高精度的可重复运动轨迹。然而，主从遥操作隔绝了术者与器械的直接物理接触，器械在血管内的受力状态必须经过从端测量与主端再现才能传递至术者^\[2\]^。因此，在测量器械操作载荷的基础上形成连续、清晰的主端力反馈，是帮助术者判断器械受阻状态的重要环节。

介入器械的力感知方案主要分为体内远端测力和体外近端测力两类，二者反映不同空间尺度的受力信息。远端测力将光纤布拉格光栅（FBG）等微型传感元件集成于器械尖端以直接感知末端接触力^\[3\]^，但受限于微细器械尺寸与封装工艺，制造成本高且难以兼容常规一次性耗材。相比之下，近端测力在体外驱动端通过传力路径中的力传感器^\[4,6\]^或驱动电机电流^\[5\]^获取沿器械传递的综合操作阻力，无需改造常规器械且便于无菌分离，但近端测力通道与机械驱动过程紧密耦合，器械真实负载与传动机构自身的运行干扰将同时作用于测量信号。

器械与驱动机构的接触方式决定了近端传力特性。滚轮摩擦驱动需维持法向预紧力，在推进与旋转复合运动时还会受到界面微滑移的影响^\[5\]^；仿人手往复夹持机构则通过面接触建立静摩擦连接^\[7\]^，便于控制夹紧力，并分别测量轴向递送力与周向旋转扭矩^\[8\]^。受直线导轨行程限制，此类机构通过主、副夹爪“夹持递送---释放回退---重新夹持”的周期性往复运动实现长距离输送^\[9,10\]^。对于承担近端测力功能的移动主爪，往复加减速引起的浮动组件惯性、旋转支路摩擦及夹爪接触切换会改变测力支路的受力平衡^\[6,8\]^，造成反馈波动。

针对近端测量中的机构附加干扰分量，现有研究主要从运行偏置标定、动力学模型补偿及数据驱动估计等方面展开。在机理建模与标定方面，Sankaran等^\[5\]^在不同转速下采集机构自由递送时的空载电流，建立运行偏置与转速的映射关系并从总力中予以扣除。Bao等^\[8\]^综合分析了摩擦、重力及旋转速度对测量结果的影响，构建了基于载荷与转速的动态补偿模型，并在时变加载实验中验证了其相较于静态零偏补偿的优势。Wang等^\[12\]^建立了递送机构的平移与旋转动力学模型，结合运动学测量实时修正测力基线，并对扭矩信号的抖动进行了滤波处理。在数据驱动建模方面，时序神经网络为表征夹持与传力过程中的复杂非线性关系提供了有效途径。Lyu等^\[13\]^将机器人运动状态、夹持间距与软体夹持器的视觉形变序列输入长短期记忆网络（LSTM），实现了器械操作力与扭矩的端到端估计；Wang等^\[14\]^采用时间卷积网络（TCN）建立了近端测量与导丝远端接触力之间的时序映射关系。

上述研究分别讨论了运行偏置校正、连续运动补偿和时序力估计，但往复夹持递送还包含主副夹爪交替承载。载荷交接、回程启停惯性以及柔顺接触的变形重建与微滑移，会与真实血管阻力变化同时出现在近端测量信号中，形成卸载台阶和附加波动。因此，需要根据往复夹持的传力过程重构连续递送时的反馈载荷，在减小换手波动的同时保留有效承载阶段新增的血管阻力变化。

# 1 问题描述（Problem description）

## 1.1 往复夹持递送过程

本文研究的夹持式血管介入机器人采用主、副双夹爪交替夹持器械，通过夹爪与器械表面的摩擦接触传递运动和载荷。主夹爪安装于沿直线导轨移动的滑台上，负责器械的轴向推进与周向旋转。主夹爪内部集成轴向与周向二自由度测力支路，用于在驱动器械的同时同步感知轴向递送力与周向旋转扭矩；副夹爪安装于近血管鞘入口端，用于在主夹爪松开与回退期间固定器械位置并承接血管端负载。

为缩短鞘口外无支撑器械长度以防止柔性导丝屈曲，系统将长距离连续递送分解为主夹爪的周期性短行程往复运动。根据控制时序与接触状态，单个周期依次经历 S1～S10 十个阶段，按操作过程归为以下四类（如图 1 所示）：

1) 稳态递送相（S1～S2）：主爪独立夹持导丝推进与旋转（S1），单次行程结束时滑台制动停止而副爪尚未闭合（S2）；

2) 卸载交接相（S3～S4）：副爪闭合建立第一次双爪共持（S3），随后主爪释放导丝并将管腔负载转移至副爪（S4）；

3) 空载回程相（S5～S6）：主爪完全脱离导丝后沿导轨高速退回（S5）并在起点制动停止（S6），期间导丝由副爪独立固定；

4) 重加载交接相（S7～S9）与稳态恢复（S10）：主爪在起点重新闭合形成第二次双爪共持（S7），副爪释放导丝（S8），随后主爪带动导丝恢复向前推进，串联柔顺传力变形逐步重建、测力响应随载荷接管而动态爬升（S9）；当重夹持后的有效推进位移达到稳定承载阈值时重加载完成，主爪恢复独立稳态承载（S10，归入稳态递送相）并进入下一周期。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig1.png){width=14.5cm}

**图 1  往复夹持递送S1～S10工作时序与物理相演变**

**Fig.1  Timing of S1--S10 stages and evolution of physical phases during reciprocating clamping delivery**

## 1.2 测力波动与补偿目标

在往复工作循环中，主夹爪交替经历承载推进与空载回退，机构运动与夹爪切换引起的附加干扰随阶段变化。主夹爪释放时，载荷向副爪转移，主爪测力支路发生阶跃卸载；快速回退时，随滑台运动的内侧浮动组件产生轴向惯性力；存在旋转运动时，旋转支路还受到惯性、轴承摩擦与阻尼的影响。重新夹持时的机械冲击，以及恢复推进初期柔顺支路的变形重建，会分别造成短暂波动和逐步恢复的测力响应。若直接将这些变化反馈至主端，术者会感受到周期性换手脉冲，影响对远端血管阻力的判断。

本文以相同初始受力状态、血管条件及有效推进与旋转轨迹下，主爪持续夹持器械时的连续递送载荷作为反馈目标。补偿量根据同步采集的运动状态、测力信号与夹持动作时序在线计算：在正常承载阶段扣除机构运动干扰，在 S4～S8 期间锁存换手前的反馈值，在 S9 期间根据实际承载与变形恢复过程重构连续递送反馈，并保留实时测力通道对新增阻力和阻力矩的响应。

全文设轴向正方向沿导丝名义中心轴指向远端血管，旋转角正方向遵循右手定则，分别采用 $\mathrm{N}$、$\mathrm{N}\cdot\mathrm{mm}$、$\mathrm{mm}$、$\mathrm{rad}$ 和 $\mathrm{s}$ 作为力、扭矩、位移、角位移和时间的单位。主爪原始测量的轴向力记为 $F_{xm}$，绕器械轴线的测量扭矩记为 $\tau_{xm}$；扭矩可由扭矩传感器直接测得，也可由切向力经标定力臂换算。补偿后的主端力与扭矩反馈量分别记为 $F_{xc}$ 和 $\tau_{xc}$。

## 1.3 本文工作

围绕往复夹持递送过程中的近端测力波动抑制问题，本文开展以下三方面研究工作：

1) 多阶段传力建模：分析主副夹爪交替承载的传力过程，建立正常递送、双爪交接与重加载阶段的动力学和串联接触刚度模型，给出浮动组件惯性、双爪共持载荷分配及弹性重加载的分析关系。

2) 物理基线与 GRU 时序残差补偿方法构建：建立扣除机构运动干扰并包含二维重加载过渡项的物理动力学基线，结合换手前稳态载荷锁存与边界平滑；引入 GRU 网络利用历史运动与时序特征在线估计物理基线与连续递送参考之间的残差，降低未建模微滑移与接触迟滞的影响。

3) 同轴参考与血管模型实验评估：在双单元同轴对拉、对扭台架上，以配对不换手试次构建连续递送载荷参考，定量评价连续力反馈重构误差、换手全周期波动及突发阻力响应，并通过消融实验分析重加载模型与残差学习的贡献；在介入血管模型中验证受压推进与旋转递送的波形。

本文其余部分组织如下：第2节建立多阶段传力模型、重加载物理过渡项与融合机理规律的 GRU 时序残差补偿方法；第3节开展同轴参考定量评估、未训练扰动测试与血管模型递送实验；第4节与第5节分别给出讨论与结论。

# 2 往复夹持传力机理与残差补偿方法（Reciprocating clamping transmission mechanism and residual compensation method）

本节围绕主、副夹爪交替承载过程，建立远端血管阻力、夹持界面传力与近端测量读数之间的关系。通过分析正常递送、双爪载荷交接及重加载过程中的轴向与旋转耦合，确定连续递送载荷与机构附加干扰项，为后续物理基线与时序残差补偿提供依据。

## 2.1 递送测量关系与交接载荷分配

对主、副夹爪共同作用的受载系统应用准静态平衡条件，忽略器械微小段的质量与分布摩擦，沿器械轴线的轴向力与绕轴扭矩满足：

$$\begin{cases}
F_M + F_S = F_{\mathrm{out}}, \\
\tau_M + \tau_S = \tau_{\mathrm{out}}
\end{cases}$$

式中，$F_{\mathrm{out}}$ 与 $\tau_{\mathrm{out}}$ 分别为远端血管对器械施加的轴向阻力与阻力矩，以阻碍推进和正转为正方向；$F_M$、$F_S$ 与 $\tau_M$、$\tau_S$ 分别为主、副夹爪施加于器械的轴向力与扭矩。定义连续递送的目标载荷向量 $\bm{w}_{\mathrm{out}} = [F_{\mathrm{out}},\tau_{\mathrm{out}}]^{\mathrm{T}}$，主、副爪载荷向量分别为 $\bm{w}_M = [F_M,\tau_M]^{\mathrm{T}}$ 与 $\bm{w}_S = [F_S,\tau_S]^{\mathrm{T}}$。在单爪独立承载的稳态递送阶段（S1、S2 及 S10），副爪完全松开，$\bm{w}_S = \bm{0}$，外载由主爪单独平衡，即 $\bm{w}_M = \bm{w}_{\mathrm{out}}$。

由于测力传感器安装在滑台上，浮动传力组件随滑台平移并随旋转机构转动，传感器原始测量向量 $\bm{y} = [F_{xm},\tau_{xm}]^{\mathrm{T}}$ 除包含器械接触载荷外，还叠加了运动部件的动力学干扰与零位偏置：

$$\bm{y} = \bm{H}_0 \bm{w}_M + \bm{d} + \bm{\varepsilon},\quad \bm{d} = \bm{p}(\bm{q}_M,\bm{c}) + \bm{b}$$

$$\bm{p}(\bm{q}_M,\bm{c}) = \begin{bmatrix}
m_s a_M \\
J_s\alpha_M+b_{v,\varphi}\omega_M+f_{c,\varphi}\operatorname{sgn}(\omega_M)
\end{bmatrix} + \bm{p}_{\mathrm{clamp}}(\bm{c})$$

式中，$\bm{H}_0 \in \mathbb{R}^{2\times2}$ 为离线标定的传递矩阵；$\bm{b}$ 为静态零偏；$\bm{\varepsilon}$ 为测量噪声；$\bm{q}_M = [x_M,\varphi_M,v_M,a_M,\omega_M,\alpha_M]^{\mathrm{T}}$ 为主爪滑台与旋转轴的运动状态（位移、转角、速度、加速度、角速度与角加速度）；$m_s$ 为轴向测力支路内侧浮动组件的质量；$J_s$ 为旋转支路的等效转动惯量；$b_{v,\varphi}$ 与 $f_{c,\varphi}$ 分别为旋转支路的黏性阻尼与库仑摩擦力矩；$\bm{p}_{\mathrm{clamp}}(\bm{c})$ 为夹爪开合动作引起的冲击分量，$\bm{c} = [c_M,c_S]^{\mathrm{T}}$ 为开合指令。

进入卸载交接（S3）与重夹持（S7）阶段时，双爪均处于闭合状态。由于夹持区覆有柔顺硅胶垫，传力支路呈现显著弹性。在准静态无宏观滑移假设下，双爪之间的短段导丝近似为刚性轴向节点。以两支路均已建立接触的平衡状态为增量起点，对主、副支路 $i\in\{M,S\}$ 有：

$$\begin{cases}
k_i = (k_{i,\mathrm{pad}}^{-1} + k_{i,\mathrm{mech}}^{-1})^{-1}, \\
\delta_i = \Delta U_i - \Delta u, \\
F_i = F_{i,0} + k_i \delta_i,\quad F_M + F_S = F_{\mathrm{out}}
\end{cases}$$

式中，$\Delta U_i$ 与 $\Delta u$ 分别为支承座和导丝节点相对于增量起点的轴向位移；$\delta_i$ 为夹爪闭合建立接触后，支承座与导丝节点之间的相对位移增量；$F_{i,0}$ 为起点处已有的轴向载荷，满足 $F_{M,0}+F_{S,0}=F_{\mathrm{out},0}$。令 $\Delta F_i=F_i-F_{i,0}$、$\Delta F_{\mathrm{out}}=F_{\mathrm{out}}-F_{\mathrm{out},0}$，由式(4)得双爪共持时的增量载荷分配关系：

$$\begin{cases}
\Delta F_M = \dfrac{k_M}{k_M+k_S}\Delta F_{\mathrm{out}} + \dfrac{k_Mk_S}{k_M+k_S}(\Delta U_M-\Delta U_S), \\
\Delta F_S = \Delta F_{\mathrm{out}}-\Delta F_M
\end{cases}$$

式(5)表明，双爪共持时新增载荷的分配取决于支路刚度比例和两支承座的相对位移增量，原有载荷则由 $F_{i,0}$ 保留。各交接阶段的承载状态如下：

1) S2 停止保持与 S3 副爪闭合阶段：S2 制动结束后，若滑台与导丝均未继续移动，主爪支路原有变形未释放，因而仍承担递送载荷。S3 副爪刚闭合时，$\Delta U_S-\Delta u\approx0$，新闭合支路尚无切向弹性变形，且 $F_{S,0}\approx0$；主爪原有预载继续保留，因此 $F_M\approx F_{\mathrm{out}}$，扣除闭合冲击后仍能测得远端血管阻力。

2) S7 主爪原地重夹持阶段：此时载荷主要由副爪承担。主爪刚闭合而尚未推进，$\Delta U_M-\Delta u\approx0$，且 $F_{M,0}\approx0$，因此主爪有效外载分量近似为零。S3 与 S7 刚闭合时出现的短暂读数波动，主要来自法向夹紧挤压硅胶垫造成的侧向膨胀及开合机械冲击，归入 $\bm{p}_{\mathrm{clamp}}(\bm{c})$，不解释为远端载荷已转移至新闭合支路。

3) S8 副爪释放阶段：当副爪松开时，一方面管腔静摩擦对静止导丝产生原地自锁作用（等效保持力记为 $F_{\mathrm{lock}} \ge 0$），限制导丝向后回退；另一方面，远端受载导丝储存的轴向弹性恢复力 $F_{\varepsilon,0}$ 驱动导丝发生微小向后回缩 $z \ge 0$ 以挤压主爪支路（产生承力 $F_{M,\mathrm{S8}} = k_M z$）时，该回缩位移同时释放了远端导丝自身的弹性压缩量（设当前血管构型下远端导丝轴向等效刚度为 $k_w$，远端推力降至 $F_{\varepsilon,0} - k_w z$）。由准静态平衡条件 $k_M z = [F_{\varepsilon,0} - F_{\mathrm{lock}} - k_w z]_{+}$ 可得：

$$z = \frac{[F_{\varepsilon,0} - F_{\mathrm{lock}}]_{+}}{k_M + k_w},\quad F_{M,\mathrm{S8}} = \frac{k_M}{k_M + k_w}[F_{\varepsilon,0} - F_{\mathrm{lock}}]_{+}$$

式中，$[a]_+=\max(a,0)$，$k_M/(k_M+k_w)$ 为串联刚度分配比例。式(6)说明，S8 末主爪被动承接的载荷受远端弹性恢复力、管腔静摩擦保持力和刚度分配比例共同影响。换手前稳态载荷非零时，S8 末实测载荷 $\widehat{F}_{M,k_9}$ 与换手前稳态载荷 $\widehat{F}_{M,k_v}$ 的比值，反映当前血管形态下远端导丝刚度 $k_w$ 与保持力 $F_{\mathrm{lock}}$ 的综合状态。因此，本文以 S8 末实测承载值 $\widehat{\bm{w}}_{M,k_9}$ 作为 S9 重加载的初始边值，结合换手前稳态载荷 $\widehat{\bm{D}}_9$ 动态确定式(10)物理基线的重加载初始补偿幅值 $\widehat{\bm{A}}_9$。$k_v$ 为 S3 前最近的稳态载荷采样时刻，$k_9$ 为 S8 结束、S9 开始的采样时刻。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig2.png){width=14.5cm}

> **【图2占位说明】**：(a) 近端二自由度测力支路与内侧浮动传力组件隔离体受力分析图，标明远端阻力反作用力、浮动组件惯性力 $m_s a_M$、旋转支路摩擦阻尼力矩及传感器敏感轴正方向；(b) 主副夹爪多级串联刚度等效模型，以及 S1（主爪独立稳态承载）、S8（副爪松开后导丝微回缩与主爪被动承接部分载荷）、S9（主爪恢复推进与旋转时的复合弹性变形重建）三个典型阶段的变形与传力演变示意图。

**图 2  测力支路受力分析及多阶段串联变形传力演变示意图**

**Fig.2  Force analysis of sensing branch and schematic of multi-stage series deformation and load transfer evolution**

## 2.2 重加载阶段的轴向与旋转耦合

在 S9 重加载阶段，轴向推进力与周向旋转扭矩由同一硅胶接触界面及其串联弹性支路共同传递。设器械接触段等效半径为 $r_e$，静摩擦系数为 $\mu_s$，接触面法向正压力积分总和为 $N_{\Sigma}$，则主爪维持无宏观滑移传力需满足椭圆极限摩擦约束：

$$F_M^2 + \left(\frac{\tau_M}{r_e}\right)^2 \le (\mu_s N_{\Sigma})^2$$

式(7)表明轴向力 $F_M$ 与扭矩 $\tau_M$ 共同占用静摩擦裕度；当复合载荷接近边界时，界面局部微滑移将使传力恢复呈现显著非线性。

以 S9 起始时刻 $k_9$ 为参考，硅胶垫、机构弹性元件与导丝段的串联变形构成二维有效变形增量 $\Delta\bm{\xi}=[\Delta\xi_x,\Delta\xi_\varphi]^{\mathrm{T}}$。在固定法向夹紧力下，用局部切线刚度表示载荷与变形关系：

$$\Delta\bm{w}_M \simeq \bm{K}\Delta\bm{\xi},\quad \bm{K} = \begin{bmatrix}
k_{xx} & k_{x\varphi} \\
k_{\varphi x} & k_{\varphi\varphi}
\end{bmatrix}$$

式中，$k_{xx}$（$\mathrm{N}/\mathrm{mm}$）与 $k_{\varphi\varphi}$（$\mathrm{N}\cdot\mathrm{mm}/\mathrm{rad}$）分别为轴向和扭转等效切线刚度，$k_{x\varphi}$（$\mathrm{N}/\mathrm{rad}$）与 $k_{\varphi x}$（$\mathrm{N}\cdot\mathrm{mm}/\mathrm{mm}$）表示两个方向的交叉耦合。

在扭矩通道中，S8 副爪松开后，导丝可能通过微小回转向主爪传递部分静态弹性扭矩。进入 S9 后，若执行复合操作（$\Delta\varphi_M\neq0$），新增转角使支路扭转变形逐步恢复，测量扭矩随之接近稳态旋转阻力矩。纯轴向推进时（$\Delta\varphi_M=0$），扭矩通道仍可能保留 S8 的静态弹性扭矩及轴向推进引起的交叉耦合增量 $k_{\varphi x}\Delta\xi_x$，因此不将该通道读数直接置零。

在固定器械、硅胶垫与法向夹紧力下，以常数特征恢复长度 $\lambda_{x0}$（$\mathrm{mm}$）和特征恢复转角 $\lambda_{\varphi0}$（$\mathrm{rad}$）描述支路从接触变形重建到稳定传力的行程尺度。这两个常数由夹持界面材料与支路刚度共同决定，通过不同载荷与速度下的恢复曲线统一拟合，并在独立试次中验证。

式(7)表明，复合递送时周向切应力会占用接触面的静摩擦裕度，可能加快切向变形的过渡。结合式(8)中的交叉刚度，定义轴向---周向耦合等效恢复行程 $s_{\mathrm{eq},k}$，描述实际承载向连续递送载荷的恢复过程：

$$\begin{gathered}
s_{x,k}=|x_{M,k}-x_{M,k_9}|,\quad s_{\varphi,k}=|\varphi_{M,k}-\varphi_{M,k_9}|, \\
s_{\mathrm{eq},k}=\sqrt{\left(\frac{s_{x,k}}{\lambda_{x0}}\right)^2+\chi_{\varphi,k}\left(\frac{s_{\varphi,k}}{\lambda_{\varphi0}}\right)^2}, \\
\frac{\mathrm{d}\bm{w}_M}{\mathrm{d}s_{\mathrm{eq}}}=\bm{D}_9-\bm{w}_M
\end{gathered}$$

式中，$s_{x,k}$ 与 $s_{\varphi,k}$ 分别为以 S8 末位置和转角为起点的恢复行程；在单向恢复段中等于累计轴向行程与累计转角。$\chi_{\varphi,k}$ 为旋转激活指示量，纯轴向推进取 0，复合递送取 1，由该恢复段的旋转指令确定，启停瞬间沿用该段取值。$s_{\mathrm{eq}}$ 无量纲。在本次短时恢复过程中，以局部稳态载荷 $\bm{D}_9=[D_{F,9},D_{\tau,9}]^{\mathrm{T}}$ 近似连续递送目标 $\bm{w}_{\mathrm{cont}}$。式(9)通过无量纲耦合恢复行程 $s_{\mathrm{eq},k}$ 将轴向与周向变形恢复过程统一表征为关于剩余未恢复载荷的一阶渐近过程。以换手前稳态估计 $\widehat{\bm{D}}_9$ 近似该目标，从 S8 末实测承载值 $\widehat{\bm{w}}_{M,k_9}$ 积分，得到连续递送目标与重加载实际承载之间的差值，作为反馈重构的补偿量：

$$\begin{cases}
\widehat{\bm{A}}_9 = \widehat{\bm{D}}_9 - \widehat{\bm{w}}_{M,k_9}, \\
\Delta\widehat{\bm{w}}_{\mathrm{reload},k} = \begin{bmatrix}
\widehat{A}_{F,9}\exp(-s_{\mathrm{eq},k}) \\
\chi_{\varphi,k}\widehat{A}_{\tau,9}\exp(-s_{\mathrm{eq},k})
\end{bmatrix}
\end{cases}$$

式中，$\widehat{\bm{D}}_9=\widehat{\bm{w}}_{M,k_v}$ 为 S3 前最近稳态窗口的载荷均值，$\widehat{\bm{A}}_9=[\widehat{A}_{F,9},\widehat{A}_{\tau,9}]^{\mathrm{T}}$ 为重构连续递送反馈所需的初始补偿幅值。纯轴向推进时，$s_{\mathrm{eq},k}=s_{x,k}/\lambda_{x0}$，式(10)退化为轴向指数恢复；同时执行推进与旋转时，$s_{\mathrm{eq},k}$ 随轴向与转角行程共同增长，反映周向剪切对纵向摩擦裕度的占用及其对恢复进程的加速作用。由于补偿量直接叠加于实时测力信号之上，当重加载期间血管阻力出现新增突变时，传感器通道仍能直接响应新增载荷，避免形成测力盲区。

## 2.3 融合机理规律的GRU时序残差补偿网络

将运动动力学补偿与重加载过渡项结合，构成由实时测量驱动的物理补偿基线。在第 $k$ 个采样时刻：

$$\begin{cases}
\widehat{\bm{d}}_k = \widehat{\bm{p}}_k + \widehat{\bm{b}}_k,\quad \widehat{\bm{w}}_{M,k} = \bm{H}_0^{-1}(\bm{y}_k - \widehat{\bm{d}}_k), \\
\bm{w}_{\mathrm{out},k}^{(0)} = \begin{bmatrix}
F_{xc,k}^{(0)} \\
\tau_{xc,k}^{(0)}
\end{bmatrix} = \widehat{\bm{w}}_{M,k} + \Delta\widehat{\bm{w}}_{\mathrm{reload},k}
\end{cases}$$

式中，$\widehat{\bm{p}}_k$ 由式(3)根据实时运动状态计算；$\Delta\widehat{\bm{w}}_{\mathrm{reload},k}$ 仅在 S9 期间计算，并在 $s_{\mathrm{eq},k}$ 超过阈值后衰减至零，其他阶段取零。

物理基线给出了显式机理补偿，但微滑移累积、接触滞回及非线性残余仍会造成偏差。为此，设计因果时序神经网络学习物理基线与理想连续递送载荷之间的残差。构造多源物理特征向量 $\bm{x}_k$ 与长度为 $N$ 的历史滑动窗口 $\bm{X}_k$：

$$\begin{cases}
\bm{x}_k = [(\bm{w}_{\mathrm{out},k}^{(0)})^{\mathrm{T}},\widehat{\bm{D}}_{9,k}^{\mathrm{T}},\bm{q}_{M,k}^{\mathrm{T}},\bm{c}_k^{\mathrm{T}},\Delta t_{e,k},\widehat{\bm{d}}_k^{\mathrm{T}}]^{\mathrm{T}}, \\
\bm{q}_{M,k} = [s_{x,k},s_{\varphi,k},v_{M,k},a_{M,k},\omega_{M,k},\alpha_{M,k}]^{\mathrm{T}}
\end{cases}$$

$$\bm{X}_k = [\bm{x}_{k-N+1},\ldots,\bm{x}_k]^{\mathrm{T}},\quad T_w = \frac{N-1}{f_s}$$

式中，$\bm{c}_k=[c_{M,k},c_{S,k}]^{\mathrm{T}}\in\{0,1\}^2$ 为开合指令（闭合取 1，释放取 0）；$\Delta t_{e,k}$ 为距最近一次经动作延迟修正的开合事件的时间；$f_s$ 为采样频率，$T_w$ 为窗口时长。输入各组维数依次为 $2+2+6+2+1+2=15$。$\widehat{\bm{D}}_{9,k}$ 在 S1/S2 采用当前低频稳态均值，进入 S3 前于 $k_v$ 锁存，在 S3～S10 保持该值，下一周期 S1 再更新。恢复行程在 $k_9$ 置零，仅在主爪承载运动时更新，S3～S8 冻结，初始 S1 以本次递送起点为参考，避免将空载回退行程作为恢复行程。

用物理基线 $\bm{w}_{\mathrm{out},k}^{(0)}$ 替代原始测量 $\bm{y}_k$，既提供当前载荷大小参考，也减少开合冲击和运动干扰直接进入网络。为进一步验证网络在滤除接触残差的同时对未知突发阻力的响应保真度，本文在第3节专门设置了独立局部阻力突变实验。由于输入已保存跨周期稳态基准和恢复行程，且 S8 末测量值已用于初始化重加载项，窗口无需覆盖整个 S4～S8 回退过程，只需覆盖短时局部动态，例如 $0.1\sim0.2\,\mathrm{s}$。实际 $N$ 由验证集选定，并在不同往复周期和操作速度下评价补偿效果。

残差学习器 $\mathcal{R}_{\theta}(\bm{X}_k)$ 由输入标准化层、$L$ 层单向 GRU 特征提取层和全连接线性输出层组成（整体框架如图 3 所示）。进入网络前，式(12)中的连续型物理分量均按训练集均值与标准差进行 Z-score 标准化，开合指令保留二值编码。对任一 GRU 层，记当前时刻输入为 $\bm{z}_k$，其门控状态更新方程为^\[26\]^：

$$\begin{cases}
\bm{g}_{r,k} = \sigma(\bm{W}_r\bm{z}_k + \bm{U}_r\bm{h}_{k-1} + \bm{b}_r), \\
\bm{g}_{z,k} = \sigma(\bm{W}_z\bm{z}_k + \bm{U}_z\bm{h}_{k-1} + \bm{b}_z), \\
\widetilde{\bm{h}}_k = \tanh[\bm{W}_h\bm{z}_k + \bm{U}_h(\bm{g}_{r,k} \odot \bm{h}_{k-1}) + \bm{b}_h], \\
\bm{h}_k = (1 - \bm{g}_{z,k}) \odot \bm{h}_{k-1} + \bm{g}_{z,k} \odot \widetilde{\bm{h}}_k
\end{cases}$$

式中，$\sigma(\cdot)$ 为 Sigmoid 激活函数，$\odot$ 为逐元素乘积；$\bm{W},\bm{U},\bm{b}$ 为可训练参数。重置门和更新门分别调节历史状态参与候选状态计算的程度及新状态的写入比例，具体取值由训练数据确定。

窗口末端第 $L$ 层隐藏状态 $\bm{h}_k^{(L)}$ 经线性输出层与反标准化映射后输出二维残差预测 $\widehat{\bm{r}}_k$。残差真值 $\bm{r}_k$、网络预测值 $\widehat{\bm{r}}_k$ 及分通道尺度归一化训练损失函数 $\mathcal{L}(\theta)$ 分别为：

$$\begin{cases}
\bm{r}_k = \begin{bmatrix}
r_{F,k} \\
r_{\tau,k}
\end{bmatrix} = \bm{w}_{\mathrm{out},k}^{(0)} - \bm{w}_{\mathrm{cont,ref},k}, \\
\widehat{\bm{r}}_k = \begin{bmatrix}
\widehat{r}_{F,k} \\
\widehat{r}_{\tau,k}
\end{bmatrix} = \mathcal{R}_{\theta}(\bm{X}_k) = \bm{W}_o\bm{h}_k^{(L)} + \bm{b}_o
\end{cases}$$

$$\mathcal{L}(\theta) = \frac{1}{|\mathcal{T}|}\sum_{k \in \mathcal{T}}\left[ \lambda_F\frac{(r_{F,k} - \widehat{r}_{F,k})^2}{s_F^2} + \lambda_{\tau}\frac{(r_{\tau,k} - \widehat{r}_{\tau,k})^2}{s_{\tau}^2} \right]$$

式中，$\bm{w}_{\mathrm{cont,ref},k}$ 为连续递送参考载荷。稳定承载的 S1、S2、S10 采用同期同轴参考载荷 $\bm{w}_{\mathrm{ref},k}$；S9 采用同一台架上配对不换手试次的参考载荷，按有效推进位置与旋转角对齐，具体配置见第3.1节。网络由此学习物理基线与连续递送目标之间的残差。$\mathcal{T}$ 仅包含上述参考有效的主爪独立承载样本；$s_F,s_\tau$ 为训练集残差标准差尺度，$\lambda_F,\lambda_\tau$ 为通道权重。线性输出层的参数包含残差的尺度恢复，使式(15)的输出单位分别为力和扭矩。

在线运行时，连续递送反馈的实时重构值为 $\widetilde{\bm{w}}_k = \bm{w}_{\mathrm{out},k}^{(0)} - \widehat{\bm{r}}_k$，全周期主端力反馈输出 $\bm{w}_{\mathrm{fb},k} = [F_{xc,k},\tau_{xc,k}]^{\mathrm{T}}$ 采用如下切换与边界平滑策略：

$$\bm{w}_{\mathrm{fb},k} = \begin{cases}
\bm{w}_{\mathrm{fb},k_v}, & s_k \in \{ \mathrm{S4},\ldots,\mathrm{S8}\}, \\
(1 - \alpha_k)\bm{w}_{\mathrm{fb},k_v} + \alpha_k\widetilde{\bm{w}}_k, & k_9 \le k \le k_9 + N_b, \\
\widetilde{\bm{w}}_k, & \text{其余时刻}
\end{cases}$$

式中，$s_k$ 表示当前工作阶段，锁存值取 S3 前 $k_v$ 时刻的反馈输出。S3 中主爪继续承载，按运动与开合模型修正测量，残差估计沿用 $k_v$ 的值；S4～S8 采用数值锁存，其中 S7 已重新接触导丝，S8 也可能被动承接载荷，但均不提前解除锁存。进入 S9 后，在 $N_b$ 个采样间隔内采用 $\alpha_k=3\zeta_k^2-2\zeta_k^3$，其中 $\zeta_k=(k-k_9)/N_b\in[0,1]$，平滑接入实时补偿输出。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig3.png){width=14.5cm}

> **【图3占位说明】**：物理基线与 GRU 残差网络融合补偿框图。左侧输入主爪运动状态与原始测力，上方支路通过运动干扰扣除与二维耦合重加载公式计算物理基线 $\bm{w}_{\mathrm{out},k}^{(0)}$；下方支路将物理基线、换手前锁存载荷 $\widehat{\bm{D}}_{9,k}$、含相对恢复行程的运动状态 $\bm{q}_{M,k}$、夹爪时序及干扰估计组成短时窗口，输入 GRU 预测残差 $\widehat{\bm{r}}_k$。物理基线减去残差后，经 S4～S8 锁存与 S9 边界平滑输出最终反馈 $\bm{w}_{\mathrm{fb},k}$。标注稳态基准的更新、锁存及 S8 末测量初始化重加载项的位置；以虚线表示离线训练时由连续递送参考 $\bm{w}_{\mathrm{cont,ref},k}$ 构造残差标签，S9 参考来自配对不换手试次。

**图 3  物理基线与GRU时序残差融合补偿框图**

**Fig.3  Compensation framework combining the physical baseline and GRU temporal residual network**

# 3 实验验证与结果分析（Experimental validation and results analysis）

## 3.1 实验装置

实验平台基于双操作手协同血管介入机器人构建，受测器械包括 0.014 英寸导引导丝与 0.035 英寸造影导丝（以及用于对比的介入导管）。近端受测单元由移动主夹爪与辅助副夹爪组成：主爪滑台通过齿轮齿条沿器械轴向（$x$ 轴）平移，两夹爪工作面均覆有柔顺硅胶垫；回弹弹簧经连杆机构提供法向闭合预紧力（$y$ 轴），直线电缸通过压杆驱动夹爪张开。主爪内部布置两个正交的单轴拉压传感器，分别测量轴向力 $F_{xm}$ 与切向力 $F_{tm}$（经有效力臂 $\ell_s$ 换算为测量扭矩 $\tau_{xm}$）；副爪沿轴向由支撑弹簧承载。

实验采用以下两套独立配置：

1) **双单元同轴参考标定与定量评估台架**。拆下血管模型，采用与受测主爪同构的第二测力操作单元作为远端随动参考端，与近端受测主、副夹爪同轴夹持器械两端。参考端全程保持夹持，通过两端运动轨迹差施加准恒定及连续变化的对拉、对扭载荷。考虑到超细柔性导丝在无管腔约束时直接受压易发生屈曲，该台架采用轴向对拉与周向对扭加载。固定夹紧条件下，硅胶垫的切向剪切变形及预滑移恢复在正、反方向上具有近似对称性，因此对拉实验可用于研究夹持支路的变形恢复与滞回；管腔内受压递送的表现则由第二套台架另行验证。

去除血管模型后，器械不受分布管壁摩擦。在副爪完全松开的 S1、S2、S9、S10 阶段，受测主爪与参考端形成直接串联受力链；在忽略中间短段器械惯性的准静态条件下，两端净载荷大小相等、方向相反。参考端读数先扣除零偏、浮动组件惯性及旋转支路摩擦阻尼，再由其独立标定的传递矩阵换算为载荷，并按受测端的坐标正方向变换符号，得到实际承载参考 $\bm{w}_{\mathrm{ref},k}$，用于描述换手后的真实卸载与恢复过程，并标定测量模型和恢复模型。

同轴台架设置换手试次与不换手参考试次。两类试次采用相同器械、夹紧条件、初始载荷、有效推进与旋转轨迹及速度，加载程序随有效递送进程重复。不换手参考段限制在单次滑台行程内，主爪持续夹持、副爪全程张开，覆盖换手前短时稳态及 S9/S10 对应的有效递送行程。配对曲线按累计有效推进位移和旋转角对齐，空载回退位移不计入递送行程，得到 S9 的连续递送参考 $\bm{w}_{\mathrm{cont,ref},k}$。以该参考训练残差网络并评价反馈重构误差；稳定承载的 S1、S2、S10 采用同期实际承载参考。

2) **介入血管模型递送验证台架**。将导丝或导管置入具有实际血管曲率的介入血管模型，不安装远端同轴夹持单元，由主、副夹爪执行连续往复推进与旋转。在 S1 稳态递送和 S9 重加载初始推进阶段设置局部阻力突变，观察受压递送时的连续反馈输出波形，验证算法在存在管壁摩擦、弯曲接触与受压递送条件下的表现。

测量与控制系统基于倍福控制总线构建，以 $f_s=250\,\mathrm{Hz}$ 同步记录测力读数、各轴运动状态（位置、速度、加速度）、两爪开合指令及控制事件。总线通信与周期计算的响应延迟经同步时钟测量后在离线处理中对齐。

## 3.2 参数辨识与多阶段物理模型验证

在双单元同轴台架上，采用已知砝码载荷和测头标定传递矩阵 $\bm{H}_0$、有效力臂 $\ell_s$ 与静态零偏 $\bm{b}$。空载状态下以不同加减速度、平移速度及旋转角速度运行滑台，通过测量数据拟合浮动组件质量 $m_s$ 以及旋转支路的阻尼 $b_{v,\varphi}$ 与摩擦 $f_{c,\varphi}$。开合动作冲击 $\bm{p}_{\mathrm{clamp}}(\bm{c})$ 由静止夹紧/释放过程记录。各支路刚度 $k_M$、$k_S$ 及远端导丝刚度 $k_w$ 由微小阶梯加载下的力---位移响应拟合，并代入式(6)验证 S8 末被动载荷分压比。特征恢复行程常数 $\lambda_{x0}$ 与 $\lambda_{\varphi0}$ 通过多组换手试次的重加载曲线拟合确定。辨识所得参数汇总于表 1。

**表 1  系统物理模型辨识参数汇总表**

**Tab.1  Summary of system physical model identification parameters**

| 参数 | 符号及量纲 | 辨识方式与数值 |
| :--- | :--- | :--- |
| 名义传递矩阵 | $\bm{H}_0$；对角元无量纲，非对角元为 $\mathrm{mm}^{-1}, \mathrm{mm}$ | 已知轴向力与扭矩联合标定；[待补] |
| 切向通道有效力臂 | $\ell_s$ ($\mathrm{mm}$) | 已知扭矩/切向力标定；[待补] |
| 浮动传力组件惯性参数 | 轴向质量 $m_s$ ($\mathrm{N}\cdot\mathrm{s}^2/\mathrm{mm}$)；转动惯量 $J_s$ ($\mathrm{N}\cdot\mathrm{mm}\cdot\mathrm{s}^2/\mathrm{rad}$) | 空载加减速运动数据拟合；[待补] |
| 旋转支路阻尼与摩擦 | 阻尼 $b_{v,\varphi}$ ($\mathrm{N}\cdot\mathrm{mm}\cdot\mathrm{s}/\mathrm{rad}$)；摩擦 $f_{c,\varphi}$ ($\mathrm{N}\cdot\mathrm{mm}$) | 多转速匀速转动数据辨识；[待补] |
| 静态零位偏置 | $\bm{b}$ ($\mathrm{N}, \mathrm{N}\cdot\mathrm{mm}$) | 静止无载状态采集；[待补] |
| 各支路等效切向刚度 | 主爪 $k_M$、副爪 $k_S$、导丝 $k_w$ ($\mathrm{N}/\mathrm{mm}$) | 阶梯位移加载曲线拟合；[待补] |
| 特征恢复行程常数 | 轴向 $\lambda_{x0}$ ($\mathrm{mm}$)；转动 $\lambda_{\varphi0}$ ($\mathrm{rad}$) | 重加载过渡曲线拟合；[待补] |
| S9/S10 评估阈值 | $\Delta x_{S9}$ ($\mathrm{mm}$) | 稳定承载判据标定；[待补] |
| 采集与通信总线周期 | $T_s = 1/f_s$ ($\mathrm{s}$) | $250\,\mathrm{Hz}$ 同步总线配置；$0.004\,\mathrm{s}$ |

在同轴台架上开展多阶段承载验证，适当延长 S3 与 S7 的持续时间，分别观测副爪刚闭合时的主爪保载现象、主爪原地重夹持时的外载近零现象，以及 S8 副爪释放后的被动载荷分压过程。实测结果表明，式(5)与式(6)能较好反映双爪共持与释放阶段的载荷分布规律。在 S9 阶段，根据式(10)计算的物理补偿量与实测恢复曲线趋势吻合，为后续时序残差补偿提供了合理的基线。

## 3.3 往复递送综合对比与消融实验

综合对比实验在双单元同轴台架与介入血管模型台架上分别开展，涵盖纯轴向递送与轴向推进---周向旋转复合递送两种主要工况。受测器械包括 0.014 英寸导引导丝与 0.035 英寸造影导丝。对比方法包括：原始测力（Raw）、传统低通滤波（LPF，截止频率与阶次根据工程常用取值设定为[待补]）、仅物理基线补偿（Physics Baseline，令式(17)中 $\widetilde{\bm{w}}_k = \bm{w}_{\mathrm{out},k}^{(0)}$）以及本文提出的物理融合 GRU 残差补偿方法（Physics + GRU）。四种方法在同轴台架上的连续力反馈重构效果对比如图 4 所示。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig4.png){width=14.5cm}

**图 4  纯轴向与复合递送工况下各方法的连续力反馈重构效果对比**

**Fig.4  Comparison of continuous force feedback reconstruction performance among methods under axial and composite delivery conditions**

在同轴台架的配对试次中，以配对不换手试次作为连续递送参考 $\bm{w}_{\mathrm{cont,ref}}$，分别计算稳态递送阶段（S1/S2/S10）与重加载阶段（S9）各方法输出的平均绝对误差（MAE）和均方根误差（RMSE）：

$$\mathrm{MAE}_{a,s} = \frac{1}{|\Omega_s|}\sum_{k \in \Omega_s}|e_{a,k}|,\quad \mathrm{RMSE}_{a,s} = \sqrt{\frac{1}{|\Omega_s|}\sum_{k \in \Omega_s}e_{a,k}^2}$$

式中，$a \in \{ F,\tau\}$ 表示评价通道，$\Omega_s$ 表示对应阶段的样本集合，$e_{a,k} = w_{\mathrm{fb},a,k} - w_{\mathrm{cont,ref},a,k}$。同时，在包含 S3～S9 完整换手与重加载过程的固定时间窗口 $\Omega_h$ 内，统计各方法输出偏离换手前稳态参考值的最大波动幅值 $E_{\mathrm{peak},a}$；并定义输出误差进入参考容差带 $\epsilon_a$ 并持续保持所需的时间为恢复时间 $t_{s,a}$：

$$\begin{cases}
E_{\mathrm{peak},a}=\max\limits_{k\in\Omega_h}|w_{\mathrm{fb},a,k}-w_{\mathrm{fb},a,k_v}|, \\
t_{s,a} = \dfrac{k_{s,a} - k_9}{f_s}, \\
k_{s,a}=\min\left\{k\in\Omega_{\mathrm{rec}}:\max\limits_{0\le j<N_s}|e_{a,k+j}|\le\epsilon_a\right\}
\end{cases}$$

式中，$\Omega_{\mathrm{rec}}$ 为重加载恢复时间搜索区间，$\epsilon_F$ 与 $\epsilon_\tau$ 为通道容差带（数值设为[待补]），$N_s/f_s$ 为连续维持时间要求。

为检验补偿方法在消除换手伪影的同时是否能够真实传递远端新增阻力，开展未训练阻力突变实验。在 S1 稳态推进阶段以及 S9 重加载初始阶段分别人工施加不同幅值和时长的突变阻力，记录各方法的输出响应，如图 5 所示。计算阻力突变峰值的保留比例与响应延迟时间。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig5.png){width=14.5cm}

> **【图5占位说明】**：(a) 同轴台架 S1 稳态递送阶段的未训练阻力突变响应，绘制参考载荷及各方法输出；(b) 同轴台架 S9 初始推进阶段的响应，分别绘制实际承载参考、配对不换手连续递送参考和各方法输出，并用对应无扰动试次提取突变增量，标注施加位置、峰值增量、保留率和响应延迟；(c) 血管模型受压递送中 S1 与 S9 局部阻力突变的原始及补偿波形，标注施加时刻。各子图明确区分两套台架，定量保留率和延迟来自同轴配对试次。

**图 5  稳态递送与重加载阶段未训练阻力突变扰动下的动态响应与保留效果**

**Fig.5  Dynamic response and preservation performance under untrained resistance disturbance injection during steady delivery and reloading stages**

进一步开展消融实验与泛化性测试，设置移除重加载过渡项（w/o Reloading Term）与纯端到端神经网络估计（Pure GRU）两组消融模型，在不同推进速度、预紧条件、器械类型及弯曲血管模型下进行测试，结果汇总于图 6，各项误差、恢复时间、保留率、延迟及推理耗时均为[待补]。

![](D:/Work_files/Vessel%20intervention%20Robot/力波动方法/write/论文撰写/JQR_LaTeX_Template-0507/fig6.png){width=14.5cm}

> **【图6占位说明】**：(a) Physics + GRU、w/o Reloading Term 与 Pure GRU 的 S9 连续反馈重构曲线，绘制配对不换手参考及局部误差，标注共同的锁存和平滑设置；(b) 分组比较 S1/S2/S10 的测量 MAE、RMSE 和 S9 的连续反馈重构 MAE、RMSE、恢复时间；(c) 按器械类型、运动速度与载荷条件列出独立测试结果，并报告批大小为 1 的在线推理耗时。两组消融均保留稳态载荷记忆和恢复行程，使用相同连续递送目标及配对数据划分；移除重加载项后重新构造标签并训练，Pure GRU 直接预测连续递送载荷。曲线、统计量及配对试次数均由实际结果填写。

**图 6  消融实验与多工况泛化性能综合评估**

**Fig.6  Comprehensive evaluation of ablation studies and multi-condition generalization performance**

# 4 讨论（Discussion）

占位占位占位占位。

# 5 结论（Conclusion）

占位占位占位占位。

**数据可用性声明**：支撑本研究的科学数据已在中国科学院科学数据银行（Science Data Bank）ScienceDB 平台公开发布，访问地址为 https://www.scidb.cn/surl/robot。

# 参考文献（References）

[1] CHEN X, YANG Y, FISCHER N, et al. Remote teleoperation of endovascular intervention robots: A systematic review[J]. IEEE Transactions on Medical Robotics and Bionics, 2026, 8(2): 579-593.

[2] GUO S, SONG Y, YIN X, et al. A novel robot-assisted endovascular catheterization system with haptic force feedback[J]. IEEE Transactions on Robotics, 2019, 35(3): 685-696.

[3] HE C, WANG S, ZUO S. A linear stepping endovascular intervention robot with variable stiffness and force sensing[J]. International Journal of Computer Assisted Radiology and Surgery, 2018, 13(5): 671-682.

[4] ZHAO Y, GUO S, XIAO N, et al. Operating force information on-line acquisition of a novel slave manipulator for vascular interventional surgery[J]. Biomedical Microdevices, 2018, 20(2): 33.

[5] SANKARAN N K, CHEMBRAMMEL P, KESAVADAS T. Force calibration for an endovascular robotic system with proximal force measurement[J]. The International Journal of Medical Robotics and Computer Assisted Surgery, 2020, 16(2): e2045.

[6] WANG K, LIU J, YAN W, et al. Force feedback controls of multi-gripper robotic endovascular intervention: design, prototype, and experiments[J]. International Journal of Computer Assisted Radiology and Surgery, 2021, 16(1): 179-192.

[7] AL-AHMAD O, OURAK M, VLEKKEN J, et al. Force control with a novel robotic catheterization system based on braided sleeve grippers[J]. IEEE Transactions on Medical Robotics and Bionics, 2023, 5(3): 602-613.

[8] BAO X, GUO S, XIAO N, et al. Compensatory force measurement and multimodal force feedback for remote-controlled vascular interventional robot[J]. Biomedical Microdevices, 2018, 20(3): 74.

[9] WANG K, YUAN H, ZENG Y, et al. Reciprocating operation method for vascular intervention surgery robot[C]//2020 IEEE International Conference on Mechatronics and Automation (ICMA). 2020: 1613-1618.

[10] CAO S, GUO S, GUO J, et al. A reciprocating delivery device-based endovascular intervention robot with multimanipulators collaboration[J]. IEEE Transactions on Instrumentation and Measurement, 2024, 73: 1-12.

[11] FISCHER J, KARSTENSEN L, MATHIS-ULLRICH F. A compact top-loading robot for endovascular interventions: Design, control and evaluation[R]. arXiv, 2026.

[12] WANG S, LIU Z, SHU X, et al. Mechanism design and force sensing of a novel cardiovascular interventional surgery robot[J]. The International Journal of Medical Robotics and Computer Assisted Surgery, 2022, 18(4): e2406.

[13] LYU C, GUO S, YAN Y, et al. Deep-learning-based force sensing method for a flexible endovascular surgery robot[J]. IEEE Transactions on Instrumentation and Measurement, 2024, 73: 1-10.

[14] WANG S, SHEN H, LIU Z, et al. Tcn-based distal force feedback strategy of a vascular interventional surgery robot[J]. IEEE Sensors Journal, 2024, 24(3): 4120-4130.

[15] GUO S, WANG Y, XIAO N, et al. Study on real-time force feedback for a master--slave interventional surgical robotic system[J]. Biomedical Microdevices, 2018, 20(2): 37.

[16] GAO W, SRINIVASAN N, PIAO D, et al. Legobot: Modular, compact, device-agnostic robot for endovascular catheter and guidewire manipulation in stroke thrombectomy[J]. IEEE/ASME Transactions on Mechatronics, 2026: 1-9.

[17] DUAN W, DU W, LI Z, et al. A high-precision positioning and force sensing robotic system for multi-instrument manipulation during robot-assisted endovascular intervention[J]. IEEE Transactions on Instrumentation and Measurement, 2026, 75: 1-14.

[18] NAZARI A A, CATANIA J, SADEGHIAN S, et al. A master--follower teleoperation system for robotic catheterisation: Design, characterisation and tracking control[J]. The International Journal of Medical Robotics and Computer Assisted Surgery, 2025, 21(3): e70073.

[19] PANTANO M, WOLF T, MATHEA P, et al. Force measurement in robot-assisted endovascular procedures: A systematic review[J]. IEEE Transactions on Medical Robotics and Bionics, 2026, 8(2): 594-611.

[20] TIEZZI P, KAO I. Modeling of viscoelastic contacts and evolution of limit surface for robotic contact interface[J]. IEEE Transactions on Robotics, 2007, 23(2): 206-217.

[21] ZHANG T, LIANG X, ZOU Y. Robot peg-in-hole assembly based on contact force estimation compensated by convolutional neural network[J]. Control Engineering Practice, 2022, 120: 105012.

[22] ZHOU Y, CHEUNG Y H, LIU S, et al. Sensorless contact forces estimation for robotic manipulators using dual-stage temporal-residual neural network compensation[J]. Control Engineering Practice, 2026, 176: 107140.

[23] YAN Y, GUO S, LIN Z, et al. Grasping-force-based passive safety method for a vascular interventional surgery robot system[J]. IEEE Transactions on Instrumentation and Measurement, 2023, 72: 1-12.

[24] PATNI S P, STOUDEK P, CHLUP H, et al. Online elasticity estimation and material sorting using standard robot grippers[J]. The International Journal of Advanced Manufacturing Technology, 2024, 132(11-12): 6033-6051.

[25] BICCHI A. On the problem of decomposing grasp and manipulation forces in multiple whole-limb manipulation[J]. Robotics and Autonomous Systems, 1994, 13(2): 127-147.

[26] CHO K, VAN MERRIËNBOER B, GULCEHRE C, et al. Learning phrase representations using rnn encoder--decoder for statistical machine translation[C]//Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP). Doha, Qatar: ACL, 2014: 1724-1734.

# 作者简介

第一作者：隋凯丞（2000--），男，博士研究生。研究领域：血管介入手术机器人，机器人力感知与控制。E-mail: suikaicheng24@mails.ucas.ac.cn。

通信作者：刘浩（1976--），男，博士，研究员，博士生导师。研究领域：医疗微创手术机器人，智能控制。E-mail: liuhao@sia.cn。

# 附录A

随录用稿提交的信息：本文基金项目的详细信息

学术论文一般不设附录。

请按表A.1填写本文的基金信息，一般仅标注省级及以上基金项目。

**表 A.1  本文基金项目信息表**

**Tab.A.1  Project funding information**

| 基金序号 | 基金全称 | 项目课题名 | 项目号 | 项目负责人 | 起止时间 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 国家自然科学基金联合基金 | 面向血管介入手术的高保真力触觉交互机理与自主递送控制 | U23A20338 | 刘浩 | 2024/01---2027/12 |
| 2 | 国家重点研发计划智能机器人专项 | 基于多源信息融合的心血管介入手术机器人精准操作技术与系统 | 2022YFB4703500 | 胡琨元 | 2022/11---2025/10 |
| 3 | 辽宁省自然科学基金优青项目 | 柔性连续体机器人非线性接触感知与主从协同控制 | 2023-MS-021 | 林鹏 | 2023/05---2026/04 |

# 附录B

正文中在介绍样机制备、实验相关材料时，往往会提及关键的材料或者产品的选用情况。此时建议在行文中添加具体某型号产品的超链接，若无超链接，请在附录B中补充生产商信息。

**表 B.1  本文产品及型号信息表**

**Tab.B.1  Product and model information**

| 产品型号（准确名称，含网络链接） | 生产商简称 | 生产商全称 | 生产商所属国家 |
| :--- | :--- | :--- | :--- |
| [SCOUT MINI](https://www.agilex.ai/chassis/11) | 松灵 | 松灵机器人（东莞）有限公司 | 中国 |
| [K823 GNSS模块](https://www.sinognss.com/product/module/k823.html) | 司南导航 | 上海司南导航技术股份有限公司 | 中国 |
| [51600](https://www.biomart.cn/infosupply/5180.htm) | Stoelting公司 | Stoelting Co. | 美国 |
