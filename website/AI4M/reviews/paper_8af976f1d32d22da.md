# 单篇论文数据集评分报告

## 待定项候选分补充

以下分数为待定项的候选分，正式分数见下方原评审记录。

### C · 候选 1 分

**对应标准**　提供了部分关键条件，但缺失会影响解读或对比。

暂选1，前提是将实验结构来源与输入结构状态视为本任务必要条件上下文的一部分，且仍需核验相关实验状态。C-1明确输入为未优化实验结构、目标为DFT优化结构的计算带隙；C-4提供CSD来源及自动去除游离溶剂的处理信息，可条件性支持部分上下文已提供，但该处理不能等同于样品的实验后处理。C-3的PBE-D3(BJ)与VASP属于计算设置，不能据此满足实验条件要求。比较相邻锚点：0所要求的必要条件缺失尚未证实；2所要求的必要实验条件完备且可追溯也未获核验。C-2仅说明合成和后处理会影响实测带隙，不能直接确立这些条件对本计算标签基准的必要性。因此1仅为上述适用性假设下的候选，尚不能形成正式评分。

**原文证据**

- C-1 · [PDF 第 6 页，正文第 12–16 行](高亮论文.pdf#page=6)

  > In this work, we have chosen to develop an ML regression model that can rapidly predict the DFT-computed
  > band gaps of MOFs. Specifically, we aim to predict the computed band gaps of the DFT-optimized
  > structures from the un-optimized, experimentally resolved MOF crystal structures such that no quantum-
  > chemical calculations need to be carried out. To achieve this, all ML models are trained on the band gaps
  > of the DFT-optimized structures but take representations of the corresponding unrelaxed experimental

- C-2 · [PDF 第 8 页，正文第 15–16 行](高亮论文.pdf#page=8)

  > (OMDB).41,65,115,116 It is also worth noting that the experimentally measured band gaps of MOFs can vary
  > by several tenths of an eV depending on the synthesis and post-treatment conditions,117 so an MAE less

- C-3 · [PDF 第 4 页，正文第 1–3 行](高亮论文.pdf#page=4)

  > carried out at the PBE-D3(BJ)27,76,77 level of theory using the Vienna ab initio Simulation Package
  > (VASP)78,79. Additional methodological details regarding the dataset construction, DFT calculations, and
  > ML methods can be found in the Supporting Information.

- C-4 · [PDF 第 3 页，正文第 34–37 行](高亮论文.pdf#page=3)

  > We considered the list of materials identified as MOFs in the Cambridge Structural Database (CSD)3,67,68
  > and the 2019 Computation-Ready, Experimental (CoRE) MOF database.4 All starting structures were taken
  > directly from the CSD,69 and free (i.e. unbound) solvents were automatically removed from the frameworks.
  > From this set of experimental crystal structures, we constructed a DFT-ready dataset of 42,362 non-

**仍需核实**

- 明确冻结的DFT带隙回归任务究竟需要哪些实验条件，以及实验结构来源与输入状态是否属于本指标认可的条件上下文。
- 核验CSD-13058-opt逐样本记录能否关联必要的合成、后处理或晶体结构测定条件及其标准化协议。
- 若样品溶剂或活化状态属于必要条件，需核验原实验样品状态与自动去除游离溶剂后的输入结构之间的对应关系。

## 原评审记录

本报告为同一模型分工评分、独立规则审查与主 Agent 裁决的结果，供后续检查；未融合专家评分。

- 论文 ID：paper_8af976f1d32d22da
- 论文名称：Machine Learning the Quantum-Chemical Properties of Metal–Organic Frameworks for Accelerated Materials Discovery with a New Electronic Structure Database
- 数据集／基准：Quantum MOF (QMOF) database；主评测子集 CSD-13058-opt
- 对应任务：在 QMOF 的 CSD-13058-opt 去重子集上，使用未优化的实验 MOF 晶体结构表示，回归预测对应 DFT 优化结构的计算带隙，并比较留出测试集表现。
- 评价对象：QMOF 数据库的 MOF 带隙回归基准：以去重的 CSD-13058-opt 子集为主要评测数据，从未优化的实验晶体结构预测 DFT 优化结构的带隙。
- 已提供的流程：从 CSD 实验晶体结构构建并筛选 QMOF，计算 DFT 性质；在 13,058 个去重样本上比较 KRR 与 CGCNN 的带隙回归结果，并报告留出测试集表现。论文另实施无监督结构分析和材料筛选案例。
- 模型：gpt-6-sol
- 思考强度：high
- 报告状态：包含待复核事项
- 高亮论文：[打开带行号与证据高亮的PDF](高亮论文.pdf)

原文检索：44 次工具调用，111 个逻辑操作（批量请求内的子操作分别计数）。

行号说明：每页从 1 开始，按阅读顺序编号；同栏、同一基线的文字片段合并。识别出的重复页眉页脚、页码和图内文字不编号；双栏注明栏位。行号为本系统生成，以带行号 PDF 阅览版为准，并非作者印刷行号。

评价对象复核：已重新核对摘要、PDF 第 3 页数据构建、第 6 页任务定义及第 7–8 页正式测试。冻结对象 CSD-13058-opt 带隙回归与原文一致；UMAP、Fe 筛选及低带隙案例均另列，不改变评价单元。

不计入本次能力判断的内容：第 5 页高自旋 Fe 与孔径筛选的阈值属于独立应用案例，不是带隙回归的约束。；第 9–11 页 UMAP 是另一项无监督任务，其聚类输出不并入带隙回归输出。；第 11–13 页低带隙材料分析属于应用案例；HSE06-D3(BJ) 是计算复核，不是实验带隙测试。；第 13 页迁移学习、多任务学习及新性质预测是未来方向。

固定任务：T-bandgap。选择依据：第 6 页明确选择从未优化实验结构预测 DFT 优化结构带隙的回归任务，第 7–8 页主要定量比较各模型在该任务上的测试结果。其他已实施的分析与筛选具有不同输出，分别登记。

## 初评、独立审查与最终裁决

## O · 输出与决策角色

**评分**：1；已评分
**对应标准**：单一性质或单一标签预测。
**判定理由**：正式基准预测单一 DFT 带隙；排序是该预测的用途。
**分档比较**：正式任务满足单一性质预测；排序仅是预测用途，生成与行动决策也未成为任务输出。
**任务归属**：T-bandgap
**边界与争议说明**：初评以排序用途取 2；独立评估以正式回归输出取 1，原文支持后者。
## A · 自适应性与序贯性

**评分**：0；已评分
**对应标准**：完全静态、一次性预测。
**判定理由**：正式协议是静态监督回归和固定集合推理，重复随机划分用于评测。
**分档比较**：固定训练、留出测试及批量预测符合 0 档；更高档所需的条件策略、主动查询或反馈更新未见于该协议。
**任务归属**：T-bandgap
**边界与争议说明**：“screening”和排序不能单独证明主动查询。
## I · 工作流整合度

**评分**：1；已评分
**对应标准**：单一模型完成单一任务。
**判定理由**：每个受评方案分别用一个模型完成同一带隙预测。
**分档比较**：单个 KRR 或 CGCNN 完成单一预测；多个特征与模型是并列受评方案，数据构建也不构成任务级串联。
**任务归属**：T-bandgap
**边界与争议说明**：独立评估将多个方案计为增强版本；原文显示它们分别受评。
## G · 目标与约束处理

**评分**：0；已评分
**对应标准**：无显式优化目标或约束。
**判定理由**：带隙为回归标签，MAE 为评测指标；建库过滤不是正式候选决策约束。
**分档比较**：正式任务只有带隙回归及误差评测；更高档的候选优化目标和任务级约束未由该流程建立。
**任务归属**：T-bandgap
**边界与争议说明**：初评把回归标签理解为单一优化目标；独立评估区分材料优化与预测评测，原文支持后者。
## U · 不确定性与失败处理

**评分**：1；已评分
**对应标准**：报告了基础不确定性，但不影响策略。
**判定理由**：Table 1 报告测试统计的一个标准差，但没有用它改变候选选择。
**分档比较**：相较只有点预测，论文另报告测试统计波动，故按基础不确定性取 1；未见候选级或策略级使用。
**任务归属**：T-bandgap
**边界与争议说明**：仅计候选预测不确定性可能取 0；此处按原锚点“基础不确定性”包含运行波动解释。
## P · 自主性与可执行性

**评分**：0；已评分
**对应标准**：仅输出预测结果。
**判定理由**：模型可自动批量预测，但未执行下一步材料或实验行动。
**分档比较**：主任务在预测输出处结束；批量推理不构成建议、行动执行或反馈规划。
**任务归属**：T-bandgap
**边界与争议说明**：自动编码和批量推理未执行材料或实验行动。
## E · 对实验结果的依赖

**评分**：1；已评分
**对应标准**：实验结果用于训练、校准或少数示例案例，但不构成正式的实验测试。
**判定理由**：训练使用实验解析结构作为输入；监督标签和正式测试参照均为 DFT 带隙。
**分档比较**：实验结构是真实训练输入，满足 1；标签与正式测试均是 DFT 值，不满足实验测试档。
**任务归属**：T-bandgap
**边界与争议说明**：若将实验结果限于目标性质测量可能取 0；原锚点未要求实验结果必须为标签。
## R · 与实验需求的对齐

**评分**：1；已评分
**对应标准**：数据明确针对某一实验需求，但未覆盖满足该需求所需的关键约束。
**判定理由**：带隙预测与导电应用相关，但作者指出低带隙不是高电导率的唯一条件。
**分档比较**：第一问为是：预测带隙关联需导电性的应用；第二问为否：低带隙并非高电导率的充分条件。
**任务归属**：T-bandgap
**边界与争议说明**：R-2 的一般材料学限定只用于限定主任务用途，不借用低带隙案例的筛选能力。
## C · 关键实验条件的完备性

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：实验结构只作输入，目标及正式测试参照均为 DFT 带隙；实验条件的适用性与追溯情况尚未确立。
**分档比较**：0 档需证实必要实验条件缺失；1 档需证实部分提供及具体缺项；2 档需关键条件可追溯。现有原文均不足。
**任务归属**：T-bandgap
**边界与争议说明**：不能因有 DFT 协议给 2，也不能因正文未列实验条件字段给 0。
## 局限与待复核事项

- C 的实验条件适用性及逐样本可追溯性未确立，故保持 pending；DFT 方法不能代替实验条件。
- R-3 属于另一低带隙案例，已从最终证据中剔除；R-2 只作通用材料学限定。
- Table 1 的图注文字支持随机划分标准差；本报告未根据表格视觉结构或图像内容推出额外结论。
- PDF 第 7 页 Table 1 图注说明测试统计为五次随机划分的均值及 ±1 标准差；未依赖表内单元格的视觉解释。

## 评分修订记录

- O：2（已评分） → 1（已评分）。
- A：分数与状态未变；修订了评分理由、证据或其他解释字段。
- I：分数与状态未变；修订了评分理由、证据或其他解释字段。
- G：1（已评分） → 0（已评分）。
- U：分数与状态未变；修订了评分理由、证据或其他解释字段。
- P：分数与状态未变；修订了评分理由、证据或其他解释字段。
- E：分数与状态未变；修订了评分理由、证据或其他解释字段。
- R：分数与状态未变；修订了评分理由、证据或其他解释字段。
- C：分数与状态未变；修订了评分理由、证据或其他解释字段。
