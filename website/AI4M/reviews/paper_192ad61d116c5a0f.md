# 单篇论文数据集评分报告

## 待定项候选分补充

以下分数为待定项的候选分，正式分数见下方原评审记录。

### E · 候选 0 分

**对应标准**　无真实实验结果；评估仅使用仿真或代理标签。

暂列候选0。E-1明确carbon-24来自10 GPa下的从头算随机结构搜索；E-2、E-3确认正式评估采用生成结构与参考结构的几何比较，但不能确定参考结构的实验来源。若其余主要数据变体也仅使用计算结构或代理标签，0比相邻的1更符合；1需要真实实验结果参与训练、校准或案例的证据，2则需要实验结果承担正式测试依据。这里不能由几何指标或摘录未提实验推断整个基准没有实验数据；其余参考结构的来源与用途尚未核实，故不能形成正式评分。

**原文证据**

- E-1 · [PDF 第 3 页，通栏第 29–34 行](高亮论文.pdf#page=3)

  > 24 atoms in the unit cell1 [15]. It was curated from a ten-times larger dataset of carbon structures
  > obtained at a pressure of 10 GPa in an ab initio random structure search [37] by choosing the
  > structures with the lowest energy per atom. The perov-5 dataset contains 18 928 perovskite structures
  > [38]. Here, each unit cell contains five atoms with varying cell sizes (all cubic in shape) and chemical
  > compositions. The MP-20 dataset contains 45 229 structures from the Materials Project with up to 20
  > atoms per unit cell spanning a diverse range of unit cell shapes and compositions [15, 39].

- E-2 · [PDF 第 3 页，通栏第 43–46 行](高亮论文.pdf#page=3)

  > Benchmarking generative models for inorganic crystal structure prediction involves generating a
  > structure for every composition in a test set. A typically reported metric is the match rate com-
  > puted using Pymatgen’s StructureMatcher module [42] which performs a one-to-one comparison
  > between the generated and reference structure. Here, the structures have to “match” only to some

- E-3 · [PDF 第 9 页，正文第 35–37 行](高亮论文.pdf#page=9)

  > We benchmark DiffCSP, FlowMM, and OMatG on our new datasets using METRe and cRMSE,
  > with cRMSE as the primary performance metric, using the standard stol= 0.5, ltol= 0.3,
  > angle_tol= 10.0 for StructureMatcher. This means that all reported cRMSE values are a

**仍需核实**

- perov-5和MP-20在各主要训练、验证及测试划分中的结构来源，以及实验测量结构的数量。
- 若含实验结构，其用于训练、校准、案例还是正式测试，以及能否分离报告实验测试性能。

### C · 候选 1 分

**对应标准**　提供了部分关键条件，但缺失会影响解读或对比。

有条件暂列候选1。C-1说明同组成可对应不同晶相，使形成条件可能影响实验参考相的解释；但这一背景不证明冻结任务使用了实验样品。C-2的10 GPa属于从头算搜索条件，C-3的容差属于计算评价设置，两者均不能充当部分实验条件的证据。候选1仅在主基准确含实验参考、且样品记录保留部分关键条件而仍不足以解释或比较多晶型的假设下成立；该假设尚待核实。相邻的0需确认必要条件确实缺失，2需确认任务所需条件完整且可追溯，目前均无充分依据。若参考结构全部来自计算，还须先解决本项实验条件要求的适用性，不能直接记0。

**原文证据**

- C-1 · [PDF 第 2 页，正文第 33–35 行](高亮论文.pdf#page=2)

  > Crystal structure prediction aims to predict stable phases from a given composition. Polymorphs
  > are distinct crystalline phases for the same chemical composition and are plentiful in the realm
  > of experimental structural synthesis. Famously, inorganic compounds such as calcium carbonate

- C-2 · [PDF 第 3 页，通栏第 29–34 行](高亮论文.pdf#page=3)

  > 24 atoms in the unit cell1 [15]. It was curated from a ten-times larger dataset of carbon structures
  > obtained at a pressure of 10 GPa in an ab initio random structure search [37] by choosing the
  > structures with the lowest energy per atom. The perov-5 dataset contains 18 928 perovskite structures
  > [38]. Here, each unit cell contains five atoms with varying cell sizes (all cubic in shape) and chemical
  > compositions. The MP-20 dataset contains 45 229 structures from the Materials Project with up to 20
  > atoms per unit cell spanning a diverse range of unit cell shapes and compositions [15, 39].

- C-3 · [PDF 第 9 页，正文第 35–37 行](高亮论文.pdf#page=9)

  > We benchmark DiffCSP, FlowMM, and OMatG on our new datasets using METRe and cRMSE,
  > with cRMSE as the primary performance metric, using the standard stol= 0.5, ltol= 0.3,
  > angle_tol= 10.0 for StructureMatcher. This means that all reported cRMSE values are a

**仍需核实**

- 主要参考结构是否关联真实实验样品，以及这些条件是否为冻结的组成条件CSP评价所必需。
- 若含实验参考，逐条核查其制备压力、温度、制备及后处理历史、结构测定方法，并确认与具体样品或标准化协议的关联及完备性。

## 原评审记录

本报告为同一模型分工评分、独立规则审查与主 Agent 裁决的结果，供后续检查；未融合专家评分。

- 论文 ID：paper_192ad61d116c5a0f
- 论文名称：All that structure matches does not glitter
- 数据集／基准：修订的 CSP 基准套件：carbon-24-unique、carbon-24-unique-N-split、perov-5-polymorph-split 和 MP-20-polymorph-split
- 对应任务：正式 CSP 任务要求受评生成模型针对给定组成输出晶体原子位置与晶格矢量；多晶型数据划分要求评价未见组成下的结构生成，生成结构按参考测试结构评估。
- 评价对象：本文修订的组成条件晶体结构预测（CSP）基准：给定测试集中的化学组成，由受评生成模型输出原子位置和晶格矢量，并在去重或按多晶型重新划分的晶体数据上比较生成结构与参考结构。
- 已提供的流程：论文对已有晶体数据去重或重新划分；正式评测 DiffCSP、FlowMM 和 OMatG 的组成条件结构生成结果；以 METRe、RMSE 和主要指标 cRMSE 比较生成结构与测试参考结构。OMatG 另进行超参数优化。
- 模型：gpt-6-sol
- 思考强度：high
- 报告状态：包含待复核事项
- 高亮论文：[打开带行号与证据高亮的PDF](高亮论文.pdf)

原文检索：37 次工具调用，167 个逻辑操作（批量请求内的子操作分别计数）。

行号说明：每页从 1 开始，按阅读顺序编号；同栏、同一基线的文字片段合并。识别出的重复页眉页脚、页码和图内文字不编号；双栏注明栏位。行号为本系统生成，以带行号 PDF 阅览版为准，并非作者印刷行号。

评价对象复核：重新核对摘要、CSP 任务定义、主要结果与附录诊断后，冻结的评价对象仍准确对应组成条件结构生成基准。三个主数据来源采用不同划分，但共享该正式任务；单结构过拟合、手性玩具测试、de novo generation 与实验规划未混入评分。冻结 profile 原样返回。其诊断环节的一个层标签存在上述语义瑕疵，不改变主任务或其证据绑定。

不计入本次能力判断的内容：不把同时生成化学组成与结构的 de novo generation 算作主 CSP 任务。；不把背景文献中的实验规划与实验室自主决策能力算入本基准。；carbon-X、carbon-NXL 和 carbon-enantiomorphs 的诊断结果不直接代表主要数据划分上的能力。；不把模型超参数搜索等同于生成候选经新结果反馈后更新的任务流程。；不把计划中的 k-METRe 视为已实施评测。

固定任务：T-CSP。选择依据：摘要和正文明确把给定组成生成结构定义为 CSP；主要结果以修订数据集上的生成模型比较及 cRMSE 为中心。

## 初评、独立审查与最终裁决

## O · 输出与决策角色

**评分**：3；已评分
**对应标准**：候选生成、逆向设计或目标导向设计。
**判定理由**：正式 CSP 任务要求受评模型依据给定组成生成晶体结构的原子位置和晶格矢量。perov-5 新划分还要求尝试生成未见组成的不同多晶型。论文未把选择下一项实验、资源或发现策略定义为该任务的输出。
**分档比较**：0 档“无实质性机器学习任务；仅数据处理或规则化处理。”与正式生成任务不符；1、2 档预测或排序不足以描述结构生成；3 档直接对应输出；4 档要求下一步候选、实验、资源或策略决策，文中正式评测仅要求生成并匹配结构。
**任务归属**：T-CSP
**边界与争议说明**：外部受评模型的生成结构是基准要求的一部分，因此不能只按数据处理给 0；模型在其他任务中的决策能力不转入本基准。
## A · 自适应性与序贯性

**评分**：1；已评分
**对应标准**：条件式预测或生成，但不根据新结果更新行为。
**判定理由**：生成以测试组成作为条件，模型对固定测试集生成结构后与参考结构比较。论文描述的 cRMSE 超参数优化用于模型选择，未将新结构结果反馈到下一轮结构候选选择。
**分档比较**：0 档“完全静态、一次性预测。”不足以涵盖给定组成的条件生成；1 档吻合。2 档要求一次性主动筛选，文中生成对象来自测试集组成；3、4 档需要任务级多轮反馈更新，附录 D 仅证实模型超参数优化。
**任务归属**：T-CSP
**边界与争议说明**：超参数优化可以使用离线评价结果，但本项衡量正式科学任务的候选行为；其优化对象和测试组成上的生成对象不同。
## I · 工作流整合度

**评分**：3；已评分
**对应标准**：多个模型或模块按顺序连接。
**判定理由**：在同一 CSP 评测流程中，受评模型先生成结构，METRe 将生成结构与参考结构匹配，cRMSE 再结合匹配覆盖和误差；OMatG 的超参数选择还使用 cRMSE。这是任务关联的模块串联，但三个生成模型是并列比较对象，且没有实验规划或候选反馈更新。
**分档比较**：0 档与已评测生成模型不符；1 档只描述单模型单任务；2 档可描述增强的单一 CSP 任务；3 档按原文“多个模型或模块按顺序连接”，生成、结构匹配、cRMSE 及 OMatG 指标驱动的超参数优化构成实际模块序列；4 档所列实验规划和反馈更新未在发现任务中连接。
**任务归属**：T-CSP
**边界与争议说明**：较窄口径可能把生成后的 METRe/cRMSE 视为单任务的增强评价而给 2；本次按“多个模型或模块按顺序连接”的字面锚点给 3。模型内部编码器数量及数据清理数量均未用于累加档位。
## G · 目标与约束处理

**评分**：1；已评分
**对应标准**：单一优化目标。
**判定理由**：cRMSE 被设为主要基准指标，OMatG 的超参数优化明确以降低 cRMSE 为目标。METRe 和 RMSE 进入这一复合指标，并非两个独立、同时权衡的正式优化目标；数据去重及多晶型划分是数据构建规则，文中亦说明报告结果未按结构或组成有效性过滤。
**分档比较**：0 档被明确的 cRMSE 优化目标排除；1 档符合已实施 OMatG 调参；2 档所需的正式任务静态候选约束不能由数据去重或匹配容差替代；3 档不能由多项报告指标推成多目标优化；4 档无动态资源约束决策。
**任务归属**：T-CSP
**边界与争议说明**：cRMSE 由 METRe 和 RMSE 组合，但论文将其作为一个主要指标和一个调参目标；给定化学组成是任务输入，不能自动提升为另一个决策约束。
## U · 不确定性与失败处理

**评分**：3；已评分
**对应标准**：显式处理噪声、失败与阴性结果。
**判定理由**：cRMSE 明确把未匹配的生成结果纳入指标并施加惩罚，处理了结构生成失败而非忽略失败样本。附录另报告不同随机种子运行的标准误，但这只是性能波动，未作为候选筛选不确定性。原文没有把未匹配等同于实验阴性结果；3 档判断仅据明确的失败惩罚机制，需重点复核其适用口径。
**分档比较**：0 档“仅输出确定性结果。”不概括运行标准误及未匹配惩罚；1 档可由运行间标准误在宽口径下支持，但其不影响策略；2 档的候选不确定性筛选未见；3 档按明确处理失败的机制由 cRMSE 支持；4 档要求不确定性驱动风险感知搜索，未建立。
**任务归属**：T-CSP
**边界与争议说明**：原锚点同时写噪声、失败与阴性结果；本证据明确覆盖生成结构未匹配这一失败类型，未证明实验阴性结果。若严格要求三类都具备，3 档将存争议，应在独立审查中检验。
## P · 自主性与可执行性

**评分**：0；已评分
**对应标准**：仅输出预测结果。
**判定理由**：正式任务中模型依据给定测试组成生成结构，评测工具把结构与参考结构匹配并计算指标。基准没有把目标设定、下一步实验或资源行动交给模型；超参数搜索属于模型开发，不能作为任务级自主行动。
**分档比较**：0 档对应模型生成预测结构；1 档需要形成行动建议，2 档需要自动执行任务级固定工作流，3 档需要按反馈选择下一步，4 档需要自主规划执行监控纠正。此处结构生成和指标计算未证明后四者。
**任务归属**：T-CSP
**边界与争议说明**：O 轴的结构生成能力与 P 轴的行动自主性不同，生成候选本身不自动构成建议、行动选择或执行。
## E · 对实验结果的依赖

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：原 carbon-24 明确来自从头算随机结构搜索，正式结果比较生成结构与参考结构的几何匹配。所供正文未确定 perov-5、MP-20 的测试参考结构是否包含历史实验测量，也未单独报告实验子集性能，因此不能据此确认整个评估对象满足 E 的任一数值档。
**分档比较**：0 档要求确认没有真实实验结果且评估仅用仿真或代理标签；现有直接来源证据仅覆盖 carbon-24。1 档要求确认实验结果进入训练、校准或案例，目前未确立。2 档要求实验结果作为正式测试依据并可单独评价；主要结果仅按数据集和模型报告几何指标，未见实验子集的单独结果。
**任务归属**：T-CSP
**边界与争议说明**：不能把 carbon-24 的计算来源推断为整套基准均无实验结果，也不能把结构匹配测试自动视为实验测试。
## R · 与实验需求的对齐

**评分**：0；已评分
**对应标准**：数据仅提供理想化性质或代理标签，与具体实验用途无关联。
**判定理由**：论文把正式基准界定为理论晶体结构生成与参考几何匹配，未把合成背景落实为某项实验决策；多晶型划分服务于生成泛化，主要评测也明确未做结构或组成有效性过滤。R 的两个固定问题在所定义正式任务中均不满足。
**分档比较**：第 0 档对应正式基准只有理论结构生成与参考匹配、没有具体实验用途；第 1 档需要明确实验需求，背景合成例子不足；第 2 档还要求相关关键约束，现有多晶型划分及未过滤的生成结果不满足。
**任务归属**：T-CSP
**边界与争议说明**：初评 NR 担心一般合成关联使用途不明；复核认为原文正面界定理论结构生成和几何匹配，背景例子没有转化为正式实验决策，故采纳独立评估的 0。
## C · 关键实验条件的完备性

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：主任务以参考晶体结构的几何匹配为正式测试，原文给出 carbon-24 的从头算搜索压力与 StructureMatcher 容差；两者都不是可追溯到实验样品的制备或测量条件。由于主基准是否使用实验测量结果及其具体实验用途尚未确定，无法先确立本任务必需的实验条件，也不能把论文未披露误作数据已证实缺失。
**分档比较**：0 档要求已证实仅有材料标识和结果且缺少解读所需条件；现有资料只是不足以核实实验条件。1、2 档都需先确立适用的关键实验条件，正分还需实验条件原文证据；目前只有计算条件与评价容差。
**任务归属**：T-CSP
**边界与争议说明**：把 10 GPa 计算搜索压力或 StructureMatcher 容差当作实验条件会错误支持正分；把未披露直接当作数据缺失又会错误支持零分。
## 局限与待复核事项

- 这是单篇论文基准的模型评价，不是专家认证结果。
- 冻结范围合同中 S-DUPLICATE-DIAGNOSTIC 的 experimental_validation 层标签与实际计算性过拟合诊断不完全相符；本报告未借该环节支持主 CSP 任务的实验能力。
- I 的顺序模块解释及 U 的生成失配惩罚口径仍有解释边界，详见逐项复核。
- perov-5 与 MP-20 参考结构的实验测量来源及样品条件未被所供材料充分确定，E 和 C 保持 pending。
- 结论依据正文与图注文字；未根据图形布局推断额外能力。Table 2 图注位于 PDF 第 10 页，区域约 [107.691,71.081,505.248,124.798]，说明不同数据划分采用的调参目标；未依赖表内单元格视觉结构。
- PDF 第 2 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 3 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 3 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 5 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 5 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 6 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 8 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 8 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 9 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 10 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 11 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 22 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 22 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 24 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 25 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 26 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准

## 评分修订记录

- R：NR（NR（信息不足）） → 0（已评分）。
