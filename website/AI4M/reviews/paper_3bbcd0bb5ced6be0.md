# 单篇论文数据集评分报告

## 评分汇总

已复核的指标采用《评分差异复核表.xlsx》的复核分，其余指标采用 Agent 评分。

| 指标 | 分数 | 评分来源 |
|---|---:|---|
| O · 输出与决策角色 | 2 | Agent |
| A · 自适应性与序贯性 | 0 | Agent |
| I · 工作流整合度 | 2 | Agent |
| G · 目标与约束处理 | 3 | 专家复核 |
| U · 不确定性与失败处理 | 0 | Agent |
| P · 自主性与可执行性 | 0 | Agent |
| E · 对实验结果的依赖 | 1 | Agent |
| R · 与实验需求的对齐 | 0 | Agent |
| C · 关键实验条件的完备性 | 1 | Agent |

## Agent 待定项候选分补充

以下为 Agent 在原评审后补充的候选分。

### C · 候选 1 分

**对应标准**　提供了部分关键条件，但缺失会影响解读或对比。

暂列候选1，但其成立依赖尚未核实的适用性假设。C-1说明主任务标签为能量、力和晶胞应力；C-2提供VASP、PAW及PBE／PBE+U等计算设置，不能将这些设置作为实验制备、加工或测量条件计分。C-3、C-4确立附属兼容性修正使用历史实验生成能，并说明其室温背景，因此存在部分实验条件信息，但不能将其直接转移为冻结主任务的条件证据。候选1须以进一步证实T1确需相关实验条件、已披露信息覆盖其中一部分，且其余条件缺口影响解读或对比为前提。相比0，现有摘录不能证明任务必需的实验条件确实缺失；相比2，尚未建立任务所需实验条件的完整性及样品或标准协议追溯。现有证据也尚未证实1所要求的实质缺口，故该候选不能作为正式评分。

**原文证据**

- C-1 · [PDF 第 2 页，正文第 26 行](高亮论文.pdf#page=2)

  > The OMat24 dataset includes a total of 118 million structures labeled with energy, forces and cell stress. The

- C-2 · [PDF 第 11 页，正文第 9–15 行](高亮论文.pdf#page=11)

  > DFT calculations generally followed Material Project default settings19 with some important exceptions. The
  > calculations in this work have been performed using the ab-initio total-energy and molecular-dynamics package
  > VASP (Vienna ab-initio simulation package) developed at the Institut für Materialphysik of the Universiät
  > Wien66,67 with periodic boundary conditions and the projector augmented wave (PAW) pseudopotentials68.
  > Exchange and correlation effects were calculated using the generalized gradient approximation and the
  > Perdew-Burke-Ernzerhof (PBE) with Hubbard U corrections for oxide and fluoride materials containing Co,
  > Cr, Fe, Mn, Mo, Ni, V, or W, following Materials Project defaults19.

- C-3 · [PDF 第 25 页，正文第 4–7 行](高亮论文.pdf#page=25)

  > In addition, an energy adjustment to certain anion species is added to account for electron localization
  > errors41. These compatiblity corrections are obtained by way of a least squares fit minimizing the error
  > between predicted formation energies and a set of experimental formation energies with reported uncertainties
  > below 100 meV/atom41.

- C-4 · [PDF 第 26 页，正文第 18–20 行](高亮论文.pdf#page=26)

  > Furthermore, we remind readers that when using MP2020 style compatiblity corrections,
  > the predicted formation energies are meant to represent values at room temperature (the temperature of
  > experimental formation energies used to fit the corrections). We refer readers to the original publication41

**仍需核实**

- 明确冻结的结构到DFT能量、力和应力预测任务是否需要实验条件；若需要，逐项说明必要条件及其影响目标解读的原因。
- 在不将附属生成焓修正并入主任务标签的前提下，提供相关实验记录与T1数据记录之间的实际关联证据。
- 若确认适用，提供测量温度、样品状态、制备加工过程和测量方法的样品字段或标准协议，并核实哪些必要条件确实缺失及其对比较的影响。

## Agent 原评审记录

Agent 使用同一模型分工评分，由独立审查和主 Agent 裁决。

- 论文 ID：paper_3bbcd0bb5ced6be0
- 论文名称：Open Materials 2024 (OMat24) Inorganic Materials Dataset and Models
- 数据集／基准：Open Materials 2024（OMat24）
- 对应任务：给定无机体相晶体原子结构，预测对应的 DFT 总能量、原子力和晶胞应力；通过 OMat24 的训练、验证及 ID、OOD、WBM 等测试划分检验预测表现。
- 评价对象：Open Materials 2024（OMat24）无机体相结构数据集支持的主任务：以晶体原子结构为输入，训练并评测机器学习原子间势对 DFT 能量、原子力和晶胞应力的预测。
- 已提供的流程：从 Alexandria 的弛豫体相结构出发，经扰动结构的 Boltzmann 抽样、从头算分子动力学和扰动后弛豫构建结构；用 DFT 标注能量、力和应力，划分训练、验证及多种测试集，训练并评测 EquiformerV2 和 eSEN 模型。论文另报告 Matbench-Discovery 下游评测及系统性软化分析。
- 模型：gpt-6-sol
- 思考强度：high
- Agent 报告状态：包含待复核事项
- 高亮论文：[打开带行号与证据高亮的PDF](高亮论文.pdf)

原文检索：124 次工具调用，146 个逻辑操作（批量请求内的子操作分别计数）。

行号说明：每页从 1 开始，按阅读顺序编号；同栏、同一基线的文字片段合并。识别出的重复页眉页脚、页码和图内文字不编号；双栏注明栏位。行号为本系统生成，以带行号 PDF 阅览版为准，并非作者印刷行号。

评价对象复核：冻结评价对象为 OMat24 的结构到 DFT 能量、力、应力预测。PDF 第 2 页给出数据标签，第 11 页明确模型输入输出，第 33 页列出主任务测试指标；第 6 页另将稳定性与热导率列为 Matbench-Discovery 任务。原评价单元成立，未将其他任务的行动或实验条件并入 T1。

不计入本次能力判断的内容：T2 稳定性发现与 T3 热导率预测虽经正式下游评测，但不把其输出或能力并入 T1 的直接监督预测任务。；扰动结构的模型能量抽样属于数据构建，不是 T1 在获得新标签后采取的下一步行动。；历史实验生成焓用于 DFT 兼容性修正及对比，不能直接当作 OMat24 主测试集的标签。；主动学习循环是未来方向；能源、碳减排等应用背景不构成本文实施的实验决策任务。

固定任务：T1。选择依据：论文将 OMat24 定义为训练 MLIP 的数据集，明确规定结构输入与能量、力、应力输出，并报告 OMat24 验证和测试指标；因此选择该直接监督任务为主评价单元。

## Agent 初评、独立审查与裁决

独立审查使用同模型新上下文，未提供初评分及专家分数；其意见供裁决，不作投票或平均。

| 指标 | 初评 | 独立审查 | Agent 裁决 |
|---|---:|---:|---:|
| O | 2 | 2 | 2 |
| A | 0 | 0 | 0 |
| I | 2 | 2 | 2 |
| G | 1 | 3 | 3 |
| U | 0 | 3 | 0 |
| P | 0 | 0 | 0 |
| E | 1 | 1 | 1 |
| R | 0 | 0 | 0 |
| C | 待复核 | 待复核 | 待复核 |

未计算加权总分：原准则未写明 O 项权重。

## O · 输出与决策角色

**评分**：2；已评分
**对应标准**：多性质预测、候选排序或风险评估。
**判定理由**：所选 T1 明确要求从输入结构预测能量、力和应力，属于多个物理量的预测。扰动候选结构的抽样发生在数据构建环节，不是 T1 的模型输出。
**分档比较**：相对 1 档，输出不止一个性质；相对 3 档，T1 不要求生成候选或逆向设计；相对 4 档，T1 不负责决定下一步实验或发现策略。
**任务归属**：T1
**边界与争议说明**：“候选”一词见于构建流程，但该流程不要求受评 T1 模型输出候选；因此不据此升至 3 或 4 档。
## A · 自适应性与序贯性

**评分**：0；已评分
**对应标准**：完全静态、一次性预测。
**判定理由**：T1 在预先标注的数据与固定测试划分上，按输入结构输出能量、力和应力预测。模型辅助抽样属于数据构建，不是任务预测后的反馈更新。
**分档比较**：0 档由固定划分上的结构到标签预测支持。普通结构输入不自动满足 1 档的条件式协议；构建阶段的一次模型辅助抽样不属于 T1 的 2 档主动筛选，也未建立 3、4 档的多轮结果反馈。
**任务归属**：T1
**边界与争议说明**：反例是从 500 个候选结构中选 5 个，但其发生在数据构建阶段，不能视为 T1 获得新标签后主动选择下一项。
## I · 工作流整合度

**评分**：2；已评分
**对应标准**：单一任务的增强版本。
**判定理由**：T1 有实际训练和评测的单模型预测流程。eSEN 同一模型先进行直接力预训练、再进行保守微调，以提高同一预测任务的精度；另测试了 DeNS 增强。它们是单任务的已实施增强，未构成独立模型或材料发现模块的任务级串联。
**分档比较**：1 档的单模型单任务成立；已实施的 eSEN 两阶段训练支持 2 档增强。3 档要求多个模型或模块按顺序连接，而这里是同一模型预训练后微调；4 档的生成、筛选、实验规划、反馈更新一体化流程未由 T1 实现。
**任务归属**：T1
**边界与争议说明**：两阶段训练可被宽泛地称为串联，但原文描述的是同一 eSEN 模型的训练状态切换和预测头移除，因此按单任务增强解释为 2 档。
## G · 目标与约束处理

**评分** 3 分（专家复核）
**对应标准**：多目标或多约束优化。
**判定理由**：EquiformerV2 在 T1 训练中分别定义能量、力与应力误差损失并共同优化，构成模型拟合层面的多目标训练。此判断不扩展为材料候选的多目标筛选；构建抽样参数也不是正式任务约束。
**分档比较**：0 档不符，因为训练目标明确；1 档把多个物理量损失概括为单一拟合目标，但原文实际分别优化能量、力、应力误差，故按 3 档的多目标口径判断。2 档静态候选约束不能从构建参数推出；4 档动态资源决策未成立。
**任务归属**：T1
**边界与争议说明**：初评把多个损失合称一个监督拟合目标；独立审查指出它们是实际训练中分别定义并优化的能量、力和应力误差。原锚点未排除训练层面的多目标优化，故采纳 3 档并限定层级。
## U · 不确定性与失败处理

**评分**：0；已评分
**对应标准**：仅输出确定性结果。
**判定理由**：T1 的正式输出是能量、力和应力点预测。DeNS 变体学习人工加入的扰动噪声；漂移力复算及严格收敛测试属于标签质量核查，未形成候选级不确定性输出或失败、阴性结果驱动的任务处理。
**分档比较**：0 档对应主任务的点预测。1 档不能由附属实验值的不确定度替代；2、4 档需要不确定性用于候选行动。3 档的噪声、失败与阴性结果处理不能由人工去噪训练和事后漂移力稳健性核查直接推出。
**任务归属**：T1
**边界与争议说明**：独立审查把去噪和漂移力复算解释为 3 档。原文第 24 页强调原样训练模型对严格收敛测试误差相近，未说明模型或发布数据依据失败／阴性结果更新处理策略；保留 0 档。
## P · 自主性与可执行性

**评分**：0；已评分
**对应标准**：仅输出预测结果。
**判定理由**：T1 的正式模型行为是给定结构并输出能量、力和应力预测。构建时的结构抽样不是由 T1 模型执行的后续任务行动。
**分档比较**：0 档与 T1 明确的预测输出相符。1 档需有任务级行动建议；2 档需自动执行相应任务流程，S3 的预构建抽样不构成该流程；3、4 档还需反馈选行动和全程监控纠正。
**任务归属**：T1
**边界与争议说明**：自动抽样发生在数据构建中；另有 T2 结构弛豫，但冻结的 T1 不承接其行动能力。
## E · 对实验结果的依赖

**评分**：1；已评分
**对应标准**：实验结果用于训练、校准或少数示例案例，但不构成正式的实验测试。
**判定理由**：论文使用历史实验生成焓拟合 OMat24 DFT 兼容性修正。所报告的实验对比是 DFT 生成焓与实验值的对比；主任务 MLIP 的 OMat24 测试指标则是能量、力和应力误差。实验数据因此用于附属校正，但原文未将其设为主任务 MLIP 的正式实验测试。
**分档比较**：0 档“无真实实验结果”不符，因为兼容性修正确实使用历史实验生成焓；1 档涵盖这一校正用途；2 档需要实验结果成为可单独评估的正式测试依据，而 Figure C.1 是 DFT 对实验的对比，Table H.1 是 MLIP 对计算标签的测试。
**任务归属**：T1
**边界与争议说明**：附属校正不是主任务的训练或测试标签，但属于论文实现的 OMat24 DFT 输出校正环节；按原准则的“校准”口径记录为 1，保留其适用范围。
## R · 与实验需求的对齐

**评分**：0；已评分
**对应标准**：数据仅提供理想化性质或代理标签，与具体实验用途无关联。
**判定理由**：固定问题一：论文明确规定的是训练 DFT 代理模型预测平衡及非平衡结构性质，未定义一种具体实验用途。固定问题二：数据限于 PBE／PBE+U 计算的周期体相结构，并明确排除缺陷、表面等效应；未给出针对某一实验用途的候选约束。实验生成焓的附属修正不能为主任务补出一个具体实验决策。
**分档比较**：0 档对应明确的 DFT 代理预测目标且无具体实验用途；1 档需先满足固定问题一，论文的广泛现实应用动机不足以定义实验用途；2 档还需与该用途对应的关键候选约束，原文的数据范围与限制未建立这种对应。
**任务归属**：T1
**边界与争议说明**：R 的两问评估实验问题及候选范围；补充材料的实验生成焓拟合说明存在实验数据使用，但不自动使主任务对应明确的实验决策。
## C · 关键实验条件的完备性

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：所选任务预测的是 DFT 能量、力和应力，论文详述的是 VASP／DFT 计算设置。附属实验生成焓修正提到室温，但未建立主任务需要哪些实验制备、加工与测量条件，也未显示这类条件如何逐样品或按标准协议连接到主任务记录。因此不能依据完整计算协议给 C 正分，也不能把论文未披露实验条件直接判作数据已证实缺失。
**分档比较**：0 档要求证实本任务必要的实验条件在数据记录中缺失，现未确立这些条件是否适用；1 档要求有部分关键实验条件且存在影响解读的缺口，室温只属于附属修正；2 档要求任务所需制备、加工、测量条件可追溯，而计算协议不能替代这些证据。三个档位均暂不能确认。
**任务归属**：T1
**边界与争议说明**：C 与 E 分别问条件完备性和实验结果使用。E 中可确认的实验校正，并不自动确定 C 所需条件或其逐样品追溯。
## 局限与待复核事项

- 本报告是依照所供论文和冻结准则作出的模型评价，未核验论文以外的数据文件或实验记录。
- A-4 与 P-3 的初评绑定跨越冻结任务环节，最终评分记录已移除这些证据；原文仍在范围核查中检查。
- C 的实验条件适用性及逐样品追溯未由所供论文确立，保留 pending。
- 已查看 PDF 第 26 页 Figure C.1 原图：横轴为实验生成焓、纵轴为 OMat24 DFT 生成焓；该图不是 MLIP 对实验标签的测试。
- PDF 第 33 页 Table H.1 仅据图注文字确认其报告能量、力、应力测试 MAE，未从表格视觉布局推断额外结论。
- PDF 第 24 页 Table B.1 的正文说明常规及严格收敛测试误差相近；未依据表格数值作独立图像解读。
- PDF 第 4 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 5 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 6 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 7 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 8 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 9 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 9 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 21 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 23 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 27 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 28 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 29 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages

## 评分修订记录

- A：分数与状态未变；修订了评分理由、证据或其他解释字段。
- G：1（已评分） → 3（已评分）。
- U：分数与状态未变；修订了评分理由、证据或其他解释字段。
- P：分数与状态未变；修订了评分理由、证据或其他解释字段。
