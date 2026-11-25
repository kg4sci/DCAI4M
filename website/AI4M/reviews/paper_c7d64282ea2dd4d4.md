# 单篇论文数据集评分报告

## 待定项候选分补充

以下分数为待定项的候选分，正式分数见下方原评审记录。

### C · 候选 1 分

**对应标准**　提供了部分关键条件，但缺失会影响解读或对比。

暂列条件性候选1，尚不能形成正式评分。C-1明确主任务为固定晶格和原子位置的虚拟组成筛选；C-2提供Quantum Espresso、赝势版本及性质对应的计算类型；C-3说明训练与评估中保持候选骨架和晶格不变。这些确立的是计算条件，不能直接视为制备、加工或实测条件。候选1成立须假设：后续确认主任务有适用的实体实验用途，并证实部分必要实验条件已有记录，但仍有影响解读或对比的缺口；当前摘录尚未验证该假设。与相邻锚点比较，0要求确认所需条件缺失，不能由未披露推得；2要求任务所需实验条件完整且可追溯，目前亦未确立。因此1仅是待补证的候选，不表示已证明实验条件部分完备。

**原文证据**

- C-1 · [PDF 第 4 页，正文第 17–23 行](高亮论文.pdf#page=4)

  > generating a crystal’s lattice, atomic positions, and compositions together, we simplify the problem such that
  > the agent only predicts the identities of the atoms given fixed lattice and atom positions. This also aligns with
  > the goal of high-throughput virtual screening (HTVS) (Jain et al., 2011), where atoms are combinatorially
  > substituted in known crystal structures and validated using DFT to design new materials computationally.
  > Hence, we formulate the RL problem with discrete action spaces. The scope of this study is limited to cubic
  > crystals (space groups 200-230) with 4-8 atoms, for which DFT calculations are faster and certain properties
  > are easier to compute.

- C-2 · [PDF 第 18 页，正文第 23–28 行](高亮论文.pdf#page=18)

  > We performed DFT single-point SCF simulations using Quantum Espresso v7.1 (Giannozzi et al., 2009),
  > which is fully open-source. Solid-state pseudopotentials from SSSP version 1.3.0 (Prandini et al., 2018) were
  > used for the calculations. The settings used are listed below.
  > 1. calculation
  > • scf for band gap and bulk modulus
  > • vc-relax for density

- C-3 · [PDF 第 15 页，正文第 21–25 行](高亮论文.pdf#page=15)

  > For practical reasons, we do not perform structure relaxation on policy-generated
  > crystals. Although DFT relaxation optimizes the crystal structure to minimize system energy, which ben-
  > efits downstream applications, it requires multiple single-point DFT calculations per sample, significantly
  > increasing computational complexity. Hence, the backbone structure and lattice of each crystal candidate
  > in the environment is unchanged during training and evaluation. As an immediate next step, we wish to

**仍需核实**

- 明确该固定结构、DFT奖励的主基准是否适用实体实验条件评价；若适用，说明具体实验用途和测量对象。
- 若存在实体实验对应关系，提供候选样品或标准协议关联的制备、加工及相应带隙、体积模量或密度测量条件。
- 提供上述实验条件的样品覆盖范围及具体缺口，以区分部分完备、完整可追溯与必要条件缺失。

## 原评审记录

本报告为同一模型分工评分、独立规则审查与主 Agent 裁决的结果，供后续检查；未融合专家评分。

- 论文 ID：paper_c7d64282ea2dd4d4
- 论文名称：CrystalGym: A New Benchmark for Materials Discovery Using Reinforcement Learning
- 数据集／基准：CrystalGym
- 对应任务：给定选定的立方晶体固定晶格及原子位置、三种性质之一的目标值，策略从空原子位开始逐步选择元素；完成晶体后由 DFT 计算对应性质并获得奖励。主评测使用混合结构、分布外目标和 18 元素动作空间。
- 评价对象：CrystalGym 基准中，以给定立方晶体晶格、原子位置和单一目标性质值为条件，由强化学习策略逐位选择元素、补全晶体组成，并利用每轮生成晶体的 DFT 性质计算结果形成奖励的任务；主要基准设置为混合起始结构、分布外目标值和 18 元素动作空间。
- 已提供的流程：环境从选定晶体结构开始，策略逐位填入元素；完成后以 DFT 计算目标性质并给出奖励，供强化学习更新。论文比较 PPO、SAC、Rainbow、DQN，并以不同结构、目标值和动作空间设置评估策略。另有取代模式实验及 LLM+REINFORCE 案例。
- 模型：gpt-6-sol
- 思考强度：high
- 报告状态：包含待复核事项
- 高亮论文：[打开带行号与证据高亮的PDF](高亮论文.pdf)

原文检索：96 次工具调用，113 个逻辑操作（批量请求内的子操作分别计数）。

行号说明：每页从 1 开始，按阅读顺序编号；同栏、同一基线的文字片段合并。识别出的重复页眉页脚、页码和图内文字不编号；双栏注明栏位。行号为本系统生成，以带行号 PDF 阅览版为准，并非作者印刷行号。

评价对象复核：已用原文第 5 页的组成补全定义、第 6 页的基准结构及第 9 页的最终评测设置复核冻结对象。正文主要任务是给定固定几何与目标性质值，逐位产生组成并由 DFT 奖励训练策略；取代模式与 LLM 案例已在冻结 profile 中单列。评价对象及完整 profile 保持冻结版本。

不计入本次能力判断的内容：不把取代模式实验 6 的 CHGNet 初始化能力并入主补全任务的通用实现。；不把 LLM+REINFORCE 案例中的 SFT 训练数据及其特殊推理限制当作所有 CrystalGym 策略的要求。；不把完整晶格与原子位置的联合生成、结构弛豫、稳定性优化或多目标强化学习视为本次主基准已实现能力。；DFT 模拟设置属于计算条件；不能据此推断制备或实测条件已被记录。

固定任务：T-completion。选择依据：第 3.1 节将从空结构逐位填入原子定义为 CrystalGym 任务；第 5 节和最终基准评测均以组成补全为中心，并明确最终采用混合结构、分布外目标及小动作空间。

## 初评、独立审查与最终裁决

## O · 输出与决策角色

**评分**：3；已评分
**对应标准**：候选生成、逆向设计或目标导向设计。
**判定理由**：正式任务要求策略在给定晶格、原子位置和目标性质值后，逐位选择元素，输出完整的候选晶体组成。逐位动作属于生成过程；正式输出不是下一项实验或资源分配决定。
**分档比较**：0 档和 1–2 档不足以描述明确要求的目标导向候选组成生成。4 档要求决定下一步候选、实验、资源或发现策略；本任务直接输出完整组成，DFT 随后按固定流程评估，未定义独立的下一项实验或资源决策。
**任务归属**：T-completion
**边界与争议说明**：强化学习确实逐步选择元素，但该选择构成一个候选组成；因此按输出角色取 3 档，而不把生成内部的每个动作重复计为 4 档。
## A · 自适应性与序贯性

**评分**：4；已评分
**对应标准**：多轮、反馈驱动的自适应闭环。
**判定理由**：晶体完成后运行 DFT、计算奖励；受评 RL 策略从不断取得的环境样本学习并改变后续选择。该在线、跨轮的生成—评估—更新过程构成反馈闭环，尽管反馈来自仿真。
**分档比较**：3 档“利用仿真或离线反馈进行多轮序贯优化”也符合 DFT 仿真奖励这一事实；4 档“多轮、反馈驱动的自适应闭环”更准确涵盖每轮生成、DFT 评价、奖励和策略更新的完整在线循环。原锚点未规定 4 档必须有实体实验反馈。
**任务归属**：T-completion
**边界与争议说明**：若将所有仿真反馈一律封顶为 3 档，会给原锚点增添未写出的实体实验必要条件。此处已评测算法的策略确实随每轮新奖励调整，故取 4 档；证据中的算法行为仅代表所评测实现。
## I · 工作流整合度

**评分**：3；已评分
**对应标准**：多个模型或模块按顺序连接。
**判定理由**：已评测实现将晶体图的 GNN 表征及 RL 策略，与完成候选后的 DFT 性质评价、奖励反馈串联起来。这是单一晶体组成补全任务中的已实现模块链；没有正式的实验规划或跨任务发现系统。
**分档比较**：2 档可描述单一任务的增强实现；3 档原文允许“多个模型或模块按顺序连接”，已评测 GNN/RL 策略和 DFT 奖励评价符合这一层级。4 档的一体化发现系统还列有筛选、实验规划等多个发现环节，本文没有将其实现为主基准工作流。
**任务归属**：T-completion
**边界与争议说明**：另一种解释会把 DFT 奖励评价视为单一 RL 任务的内部增强，仅取 2 档；但这里存在任务执行中顺序运行且相互传递结果的 GNN/RL 与 DFT 奖励模块，符合 3 档文字。此边界应在独立审查时重点复核。
## G · 目标与约束处理

**评分**：2；已评分
**对应标准**：单一目标加静态约束。
**判定理由**：每次训练分别优化一个性质靠近指定值；固定结构和小动作空间是主任务执行中生效的静态候选约束。三种性质是分开实验，不能相加为联合多目标。
**分档比较**：1 档包含单一目标，但遗漏运行时固定的元素动作空间；2 档同时覆盖该静态约束。3 档所需多目标或多约束优化没有从三个分别优化的性质和一个动作空间约束中得到证明；4 档所需动态多目标与资源约束也未建立。
**任务归属**：T-completion
**边界与争议说明**：固定晶格也限制候选范围，但 2 档已由正式执行中生效的 18 元素动作空间独立支持。失败惩罚影响奖励，不把它另计为第二个材料性质目标。
## U · 不确定性与失败处理

**评分**：3；已评分
**对应标准**：显式处理噪声、失败与阴性结果。
**判定理由**：论文报告 DFT 结果噪声及跨运行波动，并明确把 DFT 技术失败或不收敛转化为惩罚奖励。这是对失败结果的任务级显式处理；没有证据表明候选级预测不确定性驱动筛选或风险感知搜索。
**分档比较**：1 档的基础不确定性报告可由结果标准差在有限口径下体现，但它不是策略使用的预测不确定性；2 档候选筛选不确定性没有依据。3 档的失败处理有明确惩罚机制，噪声和失败也被报告；4 档要求不确定性驱动风险感知搜索，现有奖励规则未显示这一点。
**任务归属**：T-completion
**边界与争议说明**：原 3 档同时写到噪声、失败与阴性结果；本文明确处理失败，并报告噪声，但未建立独立的噪声建模或一般阴性实验机制。按协议对失败惩罚单独核查后取 3 档，此边界需重点复核。
## P · 自主性与可执行性

**评分**：3；已评分
**对应标准**：根据反馈自动选择下一步动作。
**判定理由**：人类指定性质和目标值；RL 策略自动决定各原子位的元素，环境自动完成 DFT 评价并回传奖励。已评测策略随新样本更新探索与利用，因而后续生成动作受反馈影响。流程没有自主设定研究目标或管理整个发现过程。
**分档比较**：2 档的固定生成—DFT 评价流程存在，但 3 档还得到策略依据奖励后的新样本自动改变后续原子选择的支持。4 档要求自主规划、执行、监控并纠正整个过程；用户仍设目标，计算流程预设，未见全过程自主规划。
**任务归属**：T-completion
**边界与争议说明**：DFT 奖励在轮末到达，因此同一候选内部后续原子动作不依据该轮尚未得到的奖励；3 档指跨轮更新后的下一次生成行动。
## E · 对实验结果的依赖

**评分**：0；已评分
**对应标准**：无真实实验结果；评估仅使用仿真或代理标签。
**判定理由**：主任务每轮以 DFT 计算性质并形成奖励，最终基准也以这些计算结果评估策略。Materials Project 提供起始晶体结构，但原文未将其描述为目标性质的实验测量标签或正式实验测试集。
**分档比较**：0 档对应已描述的 DFT 仿真奖励与评测。1 档需要实验结果用于训练、校准或案例；2 档需要真实实验结果作为可单独评估的正式测试依据，现有正式流程均未确立这些条件。
**任务归属**：T-completion
**边界与争议说明**：若把 Materials Project 结构的可能实验来源视为实验结果，会与原文将 DFT 计算性质用于奖励和评测的任务定义混淆；本判断仅针对正式目标标签和测试依据。
## R · 与实验需求的对齐

**评分**：0；已评分
**对应标准**：数据仅提供理想化性质或代理标签，与具体实验用途无关联。
**判定理由**：论文正式目标是比较优化 DFT 奖励的 RL 算法，性质目标分别设定。文中列举半导体、电池等广泛应用，但没有把任一目标值定义为具体实验决策；作者也明确不声称生成晶体稳定或容易合成。因此两个固定问题均未由主基准满足。
**分档比较**：固定问题一：论文列举潜在应用，但正式目标是 DFT 奖励优化，未定义具体实验用途。固定问题二：作者明确不保证稳定或易合成，候选范围也未按某项实验决策的关键约束设计。两问均否，对应 0；1 需第一问为是，2 需两问均为是。
**任务归属**：T-completion
**边界与争议说明**：若把目标性质可能用于半导体或结构材料直接算作固定问题一成立，可能倾向 1 档；原文没有指定要执行或选择的实验，因此本判断采用 0 档，并保留该边界供主 Agent 复核。
## C · 关键实验条件的完备性

**评分**：待复核；待复核
**对应标准**：当前信息不足，暂不选择数值分档
**判定理由**：主任务是固定晶格上的虚拟组成补全及 DFT 模拟评价。论文列出了计算软件和参数，却没有定义相应实体实验流程；因此无法确定哪些制备、加工和测量条件对这一任务是必要的，也不能凭论文未披露实验条件推定数据本身缺失。
**分档比较**：0 档需要证实必要实验条件确实缺失；1 档需要确定部分关键实验条件已给出但仍缺影响解读的项目；2 档需要完整、可追溯的制备加工测量条件。当前只能确认计算条件，尚不能确立实验条件适用性与必要清单，故不选择数值档位。
**任务归属**：T-completion
**边界与争议说明**：把附录 B.5 的完整 DFT 设置当成 C=2 会混淆计算与实验条件；把论文未写实体实验条件当成 C=0 则缺少已证实缺失的依据。保留 pending。
## 局限与待复核事项

- 本报告为依据当前论文与冻结准则作出的模型评估，不代表专家认证。
- DFT 成功或失败不能直接证明生成晶体可合成；论文明确不作稳定或易合成主张。
- C 项的实验条件适用性和任务所需条件清单未由当前论文确立，因此保留 pending。
- 图 1、图 2、图 6 及表 1–4 的标题和相邻正文用于定位流程与设置；本报告的判断不依赖图形内部的视觉结构，未声称完成图像视觉核查。
- PDF 第 2 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 6 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 9 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 16 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 18 页定位提示：图表区域未可靠识别；内部文字可能参与行号，核对时以带行号阅览版及图表标签为准
- PDF 第 19 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 20 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 21 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF 第 22 页定位提示：Two-column reading order is heuristic; use page rendering for ambiguous passages

## 评分修订记录

复核未修改初评分。
