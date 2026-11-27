# 单篇论文数据集评分报告

## 评分汇总

已复核的指标采用《评分差异复核表.xlsx》的复核分，其余指标采用 Agent 评分。

| 指标 | 分数 | 评分来源 |
|---|---:|---|
| O · 输出与决策角色 | 4 | 专家复核 |
| A · 自适应性与序贯性 | 3 | 专家复核 |
| I · 工作流整合度 | 3 | 专家复核 |
| G · 目标与约束处理 | 3 | 专家复核 |
| U · 不确定性与失败处理 | 1 | Agent |
| P · 自主性与可执行性 | 3 | 专家复核 |
| E · 对实验结果的依赖 | 1 | Agent |
| R · 与实验需求的对齐 | 2 | Agent |
| C · 关键实验条件的完备性 | 1 | Agent |

## Agent 待定项候选分补充

以下为 Agent 在原评审后补充的候选分。

### O · 候选 4 分

**对应标准**　对下一步候选、实验、资源分配或发现策略做出决策。

暂拟4，前提是该指标允许按非学习式计算流程的实际输出与决策角色评价。O-1支持候选生成，对应3档；O-2、O-3进一步明确，前轮排名决定哪些候选接受更长的后轮模拟，因此比仅生成候选的3档更接近4档，亦超出2档的排序输出。这里的决策限于后续计算对象，O-4明确实验子集仍由研究人员选择。另一方面，O-5描述几何规则组装，O-6描述GCMC模拟，不能据此推定机器学习任务；若0档的机器学习前提优先，候选将受影响。该适用边界尚未明确，故不能形成正式评分。

**原文证据**

- O-1 · [PDF 第 1 页，正文第 9–12 行](高亮论文.pdf#page=1)

  > computational approach to generate all conceivable MOFs from a given chemical library of building blocks (based on the
  > structures of known MOFs) and rapidly screen them to ﬁnd the best candidates for a speciﬁc application. From a library of
  > 102 building blocks we generated 137,953 hypothetical MOFs and for each one calculated the pore-size distribution,
  > surface area and methane-storage capacity. We identiﬁed over 300 MOFs with a predicted methane-storage capacity

- O-2 · [PDF 第 3 页，右栏第 85–88 行](高亮论文.pdf#page=3)

  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- O-3 · [PDF 第 4 页，通栏第 38–41 行](高亮论文.pdf#page=4)

  > Figure 4 | Adaptive three-stage screening to identify the best MOFs for methane storage. a, In the initial stage, ≏137,000 MOFs were screened for
  > methane storage at 35 bar through short simulations. b,c, The top 5% of the ﬁrst stage (b) and then the top 5% of the second stage (c), highlited in orange,
  > were recalculated using successively longer simulations, which signiﬁcantly reduced the statistical error each time. In a–c, MOFs are rank-ordered for their
  > methane adsorption abilities (best to worst runs from left to right), with statistical error indicated by purple bars. d,e, Perspective (d) and side (e) views of

- O-4 · [PDF 第 5 页，左栏第 63–67 行](高亮论文.pdf#page=5)

  > promising predicted structures (for example, ≏300 here). Thus
  > chemical experience is still useful in choosing a smaller subset for
  > which experimental synthesis can be attempted, given constraints
  > of time, cost, available laboratory equipment and reagents, among
  > other criteria. Based on our own constraints, we found a predicted

- O-5 · [PDF 第 2 页，正文第 12–15 行](高亮论文.pdf#page=2)

  > mechanical) energy minimizations are involved; the pieces are
  > connected according to the geometric rules that govern how the
  > building blocks are connected in existing MOFs. The approach is
  > very much like snapping Tinkertoys or Lego bricks together.

- O-6 · [PDF 第 2 页，正文第 29–31 行](高亮论文.pdf#page=2)

  > (experimental, pseudo and pseudo after relaxation/optimization) we
  > predicted computationally the methane adsorption isotherms at
  > 298 K using grand canonical Monte Carlo (GCMC) simulations, as

**仍需核实**

- 需明确非机器学习流程同时具有候选生成与序贯计算选择时，0档的机器学习前提与3、4档的功能描述何者优先。

### I · 候选 3 分

**对应标准**　多个模型或模块按顺序连接。

暂拟3，假设锚点中的“模块”包括几何规则生成和物理模拟模块。I-1将生成、性质计算及筛选连接为同一流程，I-2明确GCMC计算，I-3明确前轮结果用于选择后轮模拟对象，支持多个模块顺序连接。允许锚点中的另一选择是0：I-6与I-2展示的是规则组装和物理模拟，其是否属于本指标认可的工作流仍取决于机器学习前提的解释。I-4、I-5还明确实验选择依赖人员且方法不提供合成方案，不能提升为已判不满足的4档。现有证据支持模块连接，但不足以消除0与3的适用冲突。

**原文证据**

- I-1 · [PDF 第 1 页，正文第 9–12 行](高亮论文.pdf#page=1)

  > computational approach to generate all conceivable MOFs from a given chemical library of building blocks (based on the
  > structures of known MOFs) and rapidly screen them to ﬁnd the best candidates for a speciﬁc application. From a library of
  > 102 building blocks we generated 137,953 hypothetical MOFs and for each one calculated the pore-size distribution,
  > surface area and methane-storage capacity. We identiﬁed over 300 MOFs with a predicted methane-storage capacity

- I-2 · [PDF 第 2 页，正文第 29–31 行](高亮论文.pdf#page=2)

  > (experimental, pseudo and pseudo after relaxation/optimization) we
  > predicted computationally the methane adsorption isotherms at
  > 298 K using grand canonical Monte Carlo (GCMC) simulations, as

- I-3 · [PDF 第 3 页，右栏第 85–88 行](高亮论文.pdf#page=3)

  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- I-4 · [PDF 第 5 页，左栏第 63–67 行](高亮论文.pdf#page=5)

  > promising predicted structures (for example, ≏300 here). Thus
  > chemical experience is still useful in choosing a smaller subset for
  > which experimental synthesis can be attempted, given constraints
  > of time, cost, available laboratory equipment and reagents, among
  > other criteria. Based on our own constraints, we found a predicted

- I-5 · [PDF 第 6 页，左栏第 32–35 行](高亮论文.pdf#page=6)

  > screening strategy greatly accelerates its exploration. Our method
  > also does not provide, nor guarantee, a synthesis protocol for the
  > generated MOFs. Chemical intuition and synthesis experience are
  > still required to capitalize on the output from the computational

- I-6 · [PDF 第 2 页，正文第 12–15 行](高亮论文.pdf#page=2)

  > mechanical) energy minimizations are involved; the pieces are
  > connected according to the geometric rules that govern how the
  > building blocks are connected in existing MOFs. The approach is
  > very much like snapping Tinkertoys or Lego bricks together.

**仍需核实**

- 需明确I=3是否涵盖纯规则生成、GCMC模拟及筛选模块，还是必须先满足存在机器学习工作流的条件。

### C · 候选 1 分

**对应标准**　提供了部分关键条件，但缺失会影响解读或对比。

暂拟1，仅在本指标适用于冻结任务所用单例实验验证条件的假设下成立。C-1周边原文中的35 bar、298 K是全库计算筛选条件，C-2的循环数也是计算设置，均不能代替实验条件。C-3给出NOTT-107实测压力及可能活化不足的线索；C-4给出其298 K温度和图示过量吸附口径，并区分PCN-14的290 K实验，故比0档的仅有标识与结果更接近1档。但这些信息只覆盖对照材料，不能外推到137,953个假设结构；现有摘录也不足以核实样品活化、归一化及协议追溯是否完整，尚不能支持2档。C-5关于生成方法不提供合成协议的声明，不等于实验记录缺失。条件不足目前仅是待核实，正式评分仍受适用范围与记录完备性限制。

**原文证据**

- C-1 · [PDF 第 3 页，左栏第 78–80 行](高亮论文.pdf#page=3)

  > By attempting every combination of building blocks, subject to
  > the above constraints, 137,953 hypothetical MOF structures were
  > generated in total. We screened each MOF for methane storage at

- C-2 · [PDF 第 3 页，右栏第 84–88 行](高亮论文.pdf#page=3)

  > online at hmofs.northwestern.edu). Screening occurred in three
  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- C-3 · [PDF 第 5 页，右栏第 86–92 行](高亮论文.pdf#page=5)

  > We observed in experimental measurements at Northwestern
  > University that NOTT-107 had a methane storage capacity ≏8%
  > lower at 35 bar than what had been predicted by our simulations.
  > This could be attributed partly to incomplete pore activation, which
  > is corroborated by a difference between the simulated Brunauer,
  > Emmet and Teller (BET) surface area51 (2,207 m2 g21) and the
  > measured BET surface area (1,770 m2 g21). The methane adsorption

- C-4 · [PDF 第 6 页，左栏第 23–31 行](高亮论文.pdf#page=6)

  > Figure 6 | Comparison of experimental and simulated isotherms for
  > NOTT-107 and PCN 14. a,b, The organic ligand for NOTT-107 (a) is
  > structurally identical to that for PCN-14 (b) except that it bears four methyl
  > groups in the place of two fused aromatic rings. c, Comparison of excess
  > methane adsorption isotherms of NOTT-107 and PCN-14. All isotherm data
  > are at 298 K except experimental data for PCN-14 taken from ref. 40, which
  > was at 290 K. The simulations used the NOTT-107 structure generated by
  > our method (not optimized) and the PCN-14 structure determined
  > experimentally in ref. 40.

- C-5 · [PDF 第 6 页，左栏第 32–36 行](高亮论文.pdf#page=6)

  > screening strategy greatly accelerates its exploration. Our method
  > also does not provide, nor guarantee, a synthesis protocol for the
  > generated MOFs. Chemical intuition and synthesis experience are
  > still required to capitalize on the output from the computational
  > generation and screening approach. In the future, it may be possible

**仍需核实**

- 需明确以模拟标签为主体的冻结任务中，C是否适用，以及NOTT-107单例验证记录是否属于所评数据集。
- 需取得NOTT-107具体样品可追溯的制备及孔道活化协议、吸附量归一化和口径转换说明，以核实关键条件是否完整，而非从摘录未列出推定缺失。

## Agent 原评审记录

Agent 使用同一模型分工评分，由独立审查和主 Agent 裁决。

- 论文 ID：paper_819199dbc2b68f0b
- 论文名称：Large-scale screening of hypothetical metal–organic frameworks
- 数据集／基准：Hypothetical MOF database
- 对应任务：给定源自已合成MOF的构件库，按几何和组成规则生成假设结构，并基于35 bar、298 K下的甲烷储存计算结果分阶段筛选、排序候选。
- 评价对象：论文构建的假设金属有机框架（MOF）数据集及其甲烷储存候选生成与计算筛选任务：从102种构件生成137,953个假设MOF，在35 bar、298 K下筛选储存能力；NOTT-107实测属于单例验证。
- 已提供的流程：按已知MOF的连接几何组合构件并施加结构约束，生成假设MOF；计算结构性质与甲烷吸附量；用逐步加长的GCMC模拟筛选候选；由研究人员选取NOTT-107进行实验对照。
- 模型：gpt-6-sol
- 思考强度：high
- Agent 报告状态：包含待复核事项
- 高亮论文：[打开带行号与证据高亮的PDF](高亮论文.pdf)

原文检索：94 次工具调用，127 个逻辑操作（批量请求内的子操作分别计数）。

行号说明：每页从 1 开始，按阅读顺序编号；同栏、同一基线的文字片段合并。识别出的重复页眉页脚、页码和图内文字不编号；双栏注明栏位。行号为本系统生成，以带行号 PDF 阅览版为准，并非作者印刷行号。

评价对象复核：已对照摘要、第3页正式筛选定义和图4、图6原文复核冻结对象。主对象确为102种构件生成的137,953个假设MOF及35 bar、298 K甲烷储存计算筛选；NOTT-107只是单例实测验证，结构–性质趋势另属T2，未来应用不并入T1。冻结的evaluation_object与evaluation_profile保持不变。上一条回复误用了简化对象；本次恢复冻结范围。

不计入本次能力判断的内容：不把结构–性质相关性分析的输出混作主筛选任务的候选决策能力。；不把NOTT-107的单例实测对照当作137,953个候选的实验测试集。；不把人类依据时间、成本、设备和试剂所作的实验候选选择当作自动资源规划。；不把文中设想的迭代构件设计或碳捕集、储氢、分离应用算作已实现任务。

固定任务：T1。选择依据：摘要明确提出生成假设MOF并快速筛选应用候选；“Systematic screening”节将主要应用和评估限定为高压、室温甲烷储存。

## Agent 初评、独立审查与裁决

独立审查使用同模型新上下文，未提供初评分及专家分数；其意见供裁决，不作投票或平均。

| 指标 | 初评 | 独立审查 | Agent 裁决 |
|---|---:|---:|---:|
| O | 4 | 待复核 | 待复核 |
| A | 3 | 3 | 3 |
| I | 3 | 待复核 | 待复核 |
| G | 3 | 3 | 3 |
| U | 1 | 3 | 1 |
| P | 3 | 3 | 3 |
| E | 1 | 1 | 1 |
| R | 2 | 1 | 2 |
| C | 待复核 | 1 | 待复核 |

未计算加权总分：原准则未写明 O 项权重。

## O · 输出与决策角色

**评分** 4 分（专家复核）
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：T1输出生成结构、排序并据模拟排名决定下一轮计算对象；但原文生成遵循几何规则、性质由GCMC物理模拟计算，未建立实质性机器学习任务。原O=0的机器学习前提与O=3/4的输出和决策锚点在此对象上同时相关，现有准则无法唯一裁定。
**分档比较**：O=2的候选排序、O=3的候选生成和O=4的下一轮计算对象分配均有原文事实；O=0又明示无实质性机器学习任务且仅规则处理。本文的规则生成与GCMC模拟使0与高档的适用边界无法按现有文字消除，故暂挂数字。
**任务归属**：T1
**边界与争议说明**：初评4聚焦下一轮计算资源分配，独立审查暂挂聚焦非学习式实现；两者分别抓住原锚点不同句义，故接受暂挂且不发布4或0。
## A · 自适应性与序贯性

**评分** 3 分（专家复核）
**对应标准**：利用仿真或离线反馈进行多轮序贯优化。
**判定理由**：全库完成短GCMC模拟后，前7,000名进入更长模拟；第二轮前350名再次进入更长模拟。两次候选更新直接依赖上轮仿真结果，符合仿真反馈的多轮序贯优化。
**分档比较**：0档静态一次性预测、1档不据新结果更新行为和2档一次性筛选均不足以描述连续两次基于模拟排名的入选更新。3档明确容纳仿真反馈的多轮序贯优化。相较4档，本文只给出固定三阶段的重算程序，未形成实验结果或新结构生成反复进入系统并修正策略的完整闭环。
**任务归属**：T1
**边界与争议说明**：“Adaptive three-stage”只说明两次基于仿真结果的入选更新，不能仅凭adaptive字眼推到4档；但也不能因轮数预设就退回一次性筛选。
## I · 工作流整合度

**评分** 3 分（专家复核）
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：本文连接了构件生成、GCMC性质模拟和三级筛选，但没有证据显示这些环节为训练的机器学习模型。原准则I=0的“无机器学习工作流”和I=3的“多个模型或模块按顺序连接”在此存在适用边界，不能直接保留初评3。
**分档比较**：任务环节的顺序连接符合I=3的“多个模型或模块”；I=4仍缺自动实验规划与反馈。然而原I=0是“无机器学习工作流”，而已实现环节并非机器学习模型。原准则未说明是否可把此类非学习式模块串联计入I=3。
**任务归属**：T1
**边界与争议说明**：初评3强调生成、模拟、筛选模块的实际连接；独立审查暂挂指出全流程非机器学习实现，原0档前提不能忽略。
## G · 目标与约束处理

**评分** 3 分（专家复核）
**对应标准**：多目标或多约束优化。
**判定理由**：主目标是甲烷储存容量；正式生成算法分别限制无机、有机、官能团的种类数量，所有正式候选均在这些约束下生成，属于候选决策空间的多约束优化。
**分档比较**：单一甲烷容量目标加上无机、有机、官能团类别各自上限，超出2档单一目标加一条静态约束，符合3档“多约束”。4档需要动态多目标且含资源约束的决策；本文资源限制留给研究人员作实验子集选择。
**任务归属**：T1
**边界与争议说明**：这些上限确实在生成137,953个正式候选之前实施，不能只视为事后清洗；但它们都是静态构造约束，不足以满足4档动态资源决策。
## U · 不确定性与失败处理

**评分**：1；已评分
**对应标准**：报告了基础不确定性，但不影响策略。
**判定理由**：图4报告模拟结果的统计误差和长模拟可降低误差；前5%仍依甲烷吸附量排名入选。第1页原子重叠时换构件或连接点属于候选生成的几何合法性检查，不能提升为正式筛选对噪声、阴性结果或失败的任务级处理。
**分档比较**：图4显式显示模拟统计误差，满足1档的基础不确定性报告；筛选依据容量排名，未显示统计误差进入候选入选决策，故不取2。构件拼接重叠的重试属于结构生成过程的几何合法性检查，不足以作为3档任务级噪声、失败或阴性结果处理；更无4档风险感知搜索。
**任务归属**：T1
**边界与争议说明**：独立审查3据原子重叠更换构件或连接点；该机制仅处理生成步骤的几何冲突，不能证明候选评价失败被保留并用于策略。初评1以统计误差报告为依据，且明确其不是预测不确定性。
## P · 自主性与可执行性

**评分** 3 分（专家复核）
**对应标准**：根据反馈自动选择下一步动作。
**判定理由**：在固定三阶段协议内，系统自动按前轮甲烷储存模拟排名确定下一轮长模拟的具体候选。实验合成子集和实际资源安排仍由研究人员决定。
**分档比较**：系统不仅自动执行预设计算步骤，还依仿真排名确定下一轮具体重算对象，符合3档反馈选择下一动作。它未自主进行实验计划、执行、监控与纠错，人的化学经验和合成操作仍必要，故不取4。
**任务归属**：T1
**边界与争议说明**：固定轮数本身支持2档的一面；但每轮运行后的容量排名改变下一轮具体计算对象，所以选3，仅限计算动作。
## E · 对实验结果的依赖

**评分**：1；已评分
**对应标准**：实验结果用于训练、校准或少数示例案例，但不构成正式的实验测试。
**判定理由**：主体137,953个候选以模拟性质筛选；作者测量NOTT-107并与模拟容量比较，属于单例实验验证。实测结构曾用于输入或结构检查，但图2注明没有实测吸附等温线参与其比较。
**分档比较**：0档的“无真实实验结果”与NOTT-107实测不符；1档允许少数实验示例，正对应本文单例对照。2档需要真实实验结果作为正式测试依据并能在实验数据上单独评估性能；图2用实测结构作输入但没有实测吸附等温线，图6只给NOTT-107与文献PCN-14比较。
**任务归属**：T1
**边界与争议说明**：不能仅据实验来源结构判E=2，也不能忽略NOTT-107实测而判E=0；真实实验只在单例验证层面使用。
## R · 与实验需求的对齐

**评分**：2；已评分
**对应标准**：数据与候选范围支持一个明确定义的实验决策，并包含相关目标与关键约束（或通过设计保证）。
**判定理由**：固定问题一：数据目标对应为天然气车辆寻找可在35 bar、298 K高密度储存甲烷的MOF，实验用途明确。固定问题二：候选以该工况下的储存能力筛选，且构件种类数受限，使生成结构具有论文所述的合理合成复杂度。两问均有原文支持；人工选择仍需资源判断，不能把这一步算成自动决策。
**分档比较**：原准则固定两问：是否明确针对具体实验需求，是；是否覆盖与该需求相关的关键候选约束或设计保证，是，因构件几何和复杂度上限在生成中生效。1档要求缺失关键约束；虽然没有逐候选合成协议，不能抹掉已实施的候选范围约束。2档不等于保证所有候选可合成。
**任务归属**：T1
**边界与争议说明**：独立审查1强调缺少合成协议；但原文明确实施构件复杂度约束并称这些MOF是合理的合成目标。R=2仅认定候选范围与实验决策对齐，不保证个体实验成功。
## C · 关键实验条件的完备性

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：主体数据库记录的是假设结构和模拟性质；少数实验对照报告了压力、温度，并指出NOTT-107可能存在孔道活化不充分。现有正文不能确定完整数据库是否具有可追溯的样品级实验条件，或该指标应如何作用于主要为模拟标签的记录。因此不把未披露直接判为条件缺失，也不以GCMC循环数代替实验条件。
**分档比较**：C=0要求已证实仅有材料标识与结果、缺少必要条件；图6和正文至少报告单例的温度、压力，且数据库主体为模拟记录，不能从未披露推出零分。C=1要求已确立部分条件且证实缺失会影响解读或对比；活化可能影响结果，但完整记录范围不明。C=2要求关键制备、加工与测量条件可追溯至样品或统一协议；现有正文无法核实全库是否满足。
**任务归属**：T1
**边界与争议说明**：不能因论文未写出全套制备、活化步骤就认定数据库已证实缺失，也不能用GCMC循环数或单个图注代替全库实验条件完备性的证据。
## 局限与待复核事项

- O与I因非学习式实现和原准则机器学习前提的边界未决而暂挂，不能按初评分数发布。
- C缺少全库实验条件适用性与样品级协议覆盖证据，保留pending；NOTT-107单例不能替代全库条件。
- U=1只使用蒙特卡洛统计误差的基础不确定性口径，未外推为预测不确定性或风险策略。
- 本报告是依据所供论文和冻结准则作出的模型评估，不是专家认证结果。
- 已目视检查PDF第4页Figure 4：a–c依次为全库、前7,000、前350个MOF的模拟排名图；评分证据引用图注文字，未把图形误差条解释成候选级预测不确定性。
- 已目视检查PDF第6页Figure 6：c为NOTT-107与PCN-14的模拟和实验甲烷吸附等温线；温度差异由图注确认，未将两条实测曲线扩展为全库实验测试集。
- PDF 第 3 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 4 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 5 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 6 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages

## 评分修订记录

- O：4（已评分） → 待复核（待复核）。
- A：分数与状态未变；修订了评分理由、证据或其他解释字段。
- I：3（已评分） → 待复核（待复核）。
- G：分数与状态未变；修订了评分理由、证据或其他解释字段。
- U：分数与状态未变；修订了评分理由、证据或其他解释字段。
- P：分数与状态未变；修订了评分理由、证据或其他解释字段。
- E：分数与状态未变；修订了评分理由、证据或其他解释字段。
- R：分数与状态未变；修订了评分理由、证据或其他解释字段。
