# Single-Paper Dataset Scoring Report

## Score Summary

Reviewed dimensions use the reviewed scores from the Score Difference Review Table (.xlsx); other dimensions use the Agent scores.

| Dimension | Score | Source |
|---|---:|---|
| O · Output & Decision Role | 3 | Agent |
| A · Adaptivity & Sequentiality | 4 | Agent |
| I · Workflow Integration | 3 | Agent |
| G · Goal & Constraint Handling | 2 | Agent |
| U · Uncertainty & Failure Handling | 2 | Expert review |
| P · Autonomy & Actionability | 3 | Agent |
| E · Dependence on Experimental Results | 0 | Agent |
| R · Alignment with Experimental Needs | 0 | Agent |
| C · Completeness of Key Experimental Conditions | 1 | Agent |

## Agent Pending-Item Candidate Score Supplement

Below are the candidate scores the Agent added after the original review.

### C · candidate 1

**Criterion** Some key conditions are provided, but missing ones affect interpretation or comparison. 

Provisionally listed as conditional candidate 1, which cannot yet form a formal score. C-1 specifies the main task as virtual composition screening with fixed lattice and atomic positions; C-2 provides Quantum Espresso, pseudopotential versions, and the computation types corresponding to properties; C-3 states the candidate framework and lattice are kept unchanged during training and evaluation. These establish computational conditions, which cannot be directly treated as preparation, processing, or measured conditions. Candidate 1 holding must assume: subsequent confirmation that the main task has an applicable physical-experiment use, and verification that some necessary experimental conditions are recorded but gaps affecting interpretation or comparison remain; the current excerpt has not verified this assumption. Compared with adjacent anchors, 0 requires confirming the needed conditions are missing, which cannot be derived from non-disclosure; 2 requires the task's needed experimental conditions to be complete and traceable, which is also not currently established. Therefore 1 is only a candidate awaiting supplementary evidence and does not mean partial completeness of experimental conditions has been proven.

**Source evidence**

- C-1 · [PDF page 4, main text lines 17-23](highlighted_paper.pdf#page=4)

  > generating a crystal’s lattice, atomic positions, and compositions together, we simplify the problem such that
  > the agent only predicts the identities of the atoms given fixed lattice and atom positions. This also aligns with
  > the goal of high-throughput virtual screening (HTVS) (Jain et al., 2011), where atoms are combinatorially
  > substituted in known crystal structures and validated using DFT to design new materials computationally.
  > Hence, we formulate the RL problem with discrete action spaces. The scope of this study is limited to cubic
  > crystals (space groups 200-230) with 4-8 atoms, for which DFT calculations are faster and certain properties
  > are easier to compute.

- C-2 · [PDF page 18, main text lines 23-28](highlighted_paper.pdf#page=18)

  > We performed DFT single-point SCF simulations using Quantum Espresso v7.1 (Giannozzi et al., 2009),
  > which is fully open-source. Solid-state pseudopotentials from SSSP version 1.3.0 (Prandini et al., 2018) were
  > used for the calculations. The settings used are listed below.
  > 1. calculation
  > • scf for band gap and bulk modulus
  > • vc-relax for density

- C-3 · [PDF page 15, main text lines 21-25](highlighted_paper.pdf#page=15)

  > For practical reasons, we do not perform structure relaxation on policy-generated
  > crystals. Although DFT relaxation optimizes the crystal structure to minimize system energy, which ben-
  > efits downstream applications, it requires multiple single-point DFT calculations per sample, significantly
  > increasing computational complexity. Hence, the backbone structure and lattice of each crystal candidate
  > in the environment is unchanged during training and evaluation. As an immediate next step, we wish to

**Still to verify**

- Clarify whether this fixed-structure, DFT-reward main benchmark is subject to physical-experimental-condition evaluation; if so, explain the specific experimental use and measurement object.
- If a physical-experiment correspondence exists, provide the preparation and processing associated with candidate samples or standard protocols, and the corresponding band-gap, bulk-modulus, or density measurement conditions.
- Provide the sample coverage and specific gaps of the above experimental conditions, to distinguish partial completeness, full traceability, and missing necessary conditions.

## Agent Original Review Record

The Agent scores using the same model in divided roles, adjudicated by an independent review and the main Agent.

- Paper ID: paper_c7d64282ea2dd4d4
- Paper title: CrystalGym: A New Benchmark for Materials Discovery Using Reinforcement Learning
- Dataset / benchmark: CrystalGym
- Task: given a selected cubic crystal's fixed lattice and atomic positions and the target value of one of three properties, the policy starts from empty atomic sites and progressively selects elements; after completing the crystal, DFT computes the corresponding property and a reward is obtained. The main evaluation uses mixed structures, out-of-distribution targets, and an 18-element action space.
- Evaluation object: in the CrystalGym benchmark, the task where a reinforcement-learning policy, conditioned on a given cubic crystal lattice, atomic positions, and a single target property value, selects elements site by site to complete the crystal composition and forms rewards using the DFT property-computation results of each round's generated crystal; the main benchmark setting is mixed starting structures, out-of-distribution target values, and an 18-element action space.
- Provided workflow: the environment starts from a selected crystal structure, and the policy fills in elements site by site; upon completion, DFT computes the target property and gives a reward for reinforcement-learning updating. The paper compares PPO, SAC, Rainbow, and DQN, and evaluates policies with different structure, target-value, and action-space settings. There are also substitution-mode experiments and an LLM+REINFORCE case.
- Model: gpt-6-sol
- Reasoning effort: high
- Agent report status: contains items pending review
- Highlighted paper: [open the line-numbered, evidence-highlighted PDF](highlighted_paper.pdf)

Source retrieval: 96 tool calls, 113 logical operations (sub-operations within batch requests counted separately).

Line-number note: each page starts at 1, numbered in reading order; text fragments in the same column and on the same baseline are merged. Detected repeated headers/footers, page numbers, and in-figure text are not numbered; columns are marked for two-column layouts. Line numbers are generated by this system, based on the line-numbered PDF reading copy, not the authors printed line numbers.

Evaluation object review: Re-checked the frozen object using the composition-completion definition on source page 5, the benchmark structure on page 6, and the final evaluation setup on page 9. The main task in the text is, given fixed geometry and target property values, to generate composition site by site and train the policy with DFT rewards; the substitution mode and LLM case are separately listed in the frozen profile. The evaluation object and complete profile keep the frozen version.

Content excluded from this capability assessment: The CHGNet initialization capability of substitution-mode experiment 6 is not merged into the general implementation of the main completion task.; The SFT training data and its special inference restrictions in the LLM+REINFORCE case are not treated as requirements for all CrystalGym policies.; Joint generation of complete lattice and atomic positions, structure relaxation, stability optimization, or multi-objective reinforcement learning are not treated as capabilities implemented in this main benchmark.; DFT simulation settings are computational conditions; it cannot be inferred from them that preparation or measured conditions have been recorded.

Fixed task: T-completion. Selection rationale: Section 3.1 defines filling atoms site by site from an empty structure as the CrystalGym task; Section 5 and the final benchmark evaluation both center on composition completion, and explicitly adopt mixed structures, out-of-distribution targets, and a small action space in the end.

## Agent Initial Scoring, Independent Review & Adjudication

The independent review uses a fresh context of the same model, without the initial scores or expert scores; its opinion informs adjudication, not voting or averaging.

| Dimension | Initial | Independent review | Agent adjudication |
|---|---:|---:|---:|
| O | 3 | 3 | 3 |
| A | 4 | 4 | 4 |
| I | 3 | 3 | 3 |
| G | 2 | 2 | 2 |
| U | 3 | 3 | 3 |
| P | 3 | 3 | 3 |
| E | 0 | 0 | 0 |
| R | 0 | 0 | 0 |
| C | pending review | pending review | pending review |

Weighted total not computed: the original rubric did not specify the weight for O.

## O · Output & Decision Role

**Score**: 3; scored
**Criterion**: Candidate generation, inverse design, or goal-directed design. 
**Rationale**: The formal task requires the policy, after given lattice, atomic positions, and target property values, to select elements site by site and output complete candidate crystal compositions. Site-by-site actions belong to the generation process; the formal output is not a next experiment or resource allocation decision.
**Level comparison**: Levels 0 and 1-2 are insufficient to describe the explicitly required goal-directed candidate composition generation. Level 4 requires deciding the next candidates, experiments, resources, or discovery strategy; this task directly outputs complete compositions, and DFT subsequently evaluates them in a fixed workflow, without defining an independent next experiment or resource decision.
**Task**: T-completion
**Boundary & dispute notes**: Reinforcement learning does select elements step by step, but that selection constitutes one candidate composition; therefore level 3 is taken by output role, without repeatedly counting each internal generation action as level 4.
## A · Adaptivity & Sequentiality

**Score**: 4; scored
**Criterion**: Multi-round, feedback-driven adaptive closed loop. 
**Rationale**: After crystal completion DFT is run and rewards computed; the evaluated RL policy learns from continuously obtained environment samples and changes subsequent selection. This online, cross-round generation-evaluation-updating process constitutes a feedback closed loop, although the feedback comes from simulation.
**Level comparison**: Level 3 "Multi-round sequential optimization using simulation or offline feedback" also fits the fact of DFT simulation reward; level 4 "Multi-round, feedback-driven adaptive closed loop" more accurately covers the complete online loop of each round's generation, DFT evaluation, reward, and policy update. The original anchor does not stipulate that level 4 must have physical experiment feedback.
**Task**: T-completion
**Boundary & dispute notes**: Capping all simulation feedback uniformly at level 3 would add an unwritten physical-experiment necessary condition to the original anchor. Here the evaluated algorithm's strategy does adjust with each round's new reward, so level 4 is taken; the algorithm behavior in the evidence only represents the evaluated implementation.
## I · Workflow Integration

**Score**: 3; scored
**Criterion**: Multiple models or modules connected in sequence. 
**Rationale**: The evaluated implementation chains the crystal graph's GNN representation and RL policy with DFT property evaluation and reward feedback after candidate completion. This is an implemented module chain in a single crystal composition completion task; there is no formal experiment planning or cross-task discovery system.
**Level comparison**: Level 2 can describe an enhanced implementation of a single task; level 3's source allows "Multiple models or modules connected in sequence", and the evaluated GNN/RL policy and DFT reward evaluation fit this level. Level 4's integrated discovery system also lists screening, experiment planning, and other discovery stages, which this paper does not implement as the main benchmark workflow.
**Task**: T-completion
**Boundary & dispute notes**: Another interpretation would treat DFT reward evaluation as an internal enhancement of a single RL task, taking only level 2; but here there are GNN/RL and DFT reward modules that run sequentially and pass results to each other during task execution, fitting the level-3 wording. This boundary should be focused on during the Independent review.
## G · Goal & Constraint Handling

**Score**: 2; scored
**Criterion**: A single objective with static constraints. 
**Rationale**: Each training separately optimizes one property toward a specified value; fixed structure and small action space are static candidate constraints taking effect during main-task execution. The three properties are separate experiments and cannot be summed into joint multi-objectives.
**Level comparison**: Level 1 contains a single objective but misses the runtime-fixed element action space; level 2 covers that static constraint simultaneously. The multi-objective or multi-constraint optimization required by level 3 is not proven from three separately optimized properties and one action-space constraint; the dynamic multi-objective and resource constraints required by level 4 are also not established.
**Task**: T-completion
**Boundary & dispute notes**: A fixed lattice also limits the candidate scope, but level 2 is independently supported by the 18-element action space effective in formal execution. The failure penalty affects the reward and is not separately counted as a second materials-property objective.
## U · Uncertainty & Failure Handling

**Score** 2(Expert review)
**Criterion**: Noise, failures, and negative results are explicitly handled. 
**Rationale**: The paper reports DFT result noise and cross-run fluctuation, and explicitly converts DFT technical failures or non-convergence into penalty rewards. This is task-level explicit handling of failed results; there is no evidence that candidate-level predictive uncertainty drives screening or risk-aware search.
**Level comparison**: Level 1's basic uncertainty reporting can be embodied by result standard deviation under a limited scope, but it is not prediction uncertainty used by the strategy; level 2's candidate-screening uncertainty has no basis. Level 3's failure handling has a clear penalty mechanism, and noise and failure are also reported; level 4 requires uncertainty-driven risk-aware search, which the existing reward rules do not show.
**Task**: T-completion
**Boundary & dispute notes**: The original level 3 writes noise, failures, and negative results together; this paper explicitly handles failures and reports noise, but does not establish independent noise modeling or a general negative-experiment mechanism. After separately checking the failure penalty per the protocol, level 3 is taken; this boundary needs focused review.
## P · Autonomy & Actionability

**Score**: 3; scored
**Criterion**: Automatically selects the next action based on feedback. 
**Rationale**: Humans specify properties and target values; the RL policy automatically decides the element at each atomic site, and the environment automatically completes DFT evaluation and returns rewards. The evaluated policy updates exploration and exploitation with new samples, so subsequent generation actions are affected by feedback. The workflow does not autonomously set research objectives or manage the whole discovery process.
**Level comparison**: Level 2's fixed generation-DFT evaluation workflow exists, but level 3 is additionally supported by the policy automatically changing subsequent atom selection based on new samples after reward. Level 4 requires autonomously planning, executing, monitoring, and correcting the whole process; the user still sets the objective, the computational workflow is preset, and no whole-process autonomous planning is seen.
**Task**: T-completion
**Boundary & dispute notes**: The DFT reward arrives at the end of the round, so subsequent atomic actions within the same candidate do not rely on the reward not yet obtained in that round; level 3 refers to the next generation action after cross-round updating.
## E · Dependence on Experimental Results

**Score**: 0; scored
**Criterion**: No real experimental results; evaluation uses only simulation or proxy labels. 
**Rationale**: The main task computes properties via DFT each round and forms rewards, and the final benchmark also evaluates policies with these computational results. Materials Project provides starting crystal structures, but the source does not describe them as experimental measurement labels of target properties or a formal experimental test set.
**Level comparison**: Level 0 corresponds to the described DFT simulation reward and evaluation. Level 1 requires experimental results used for training, calibration, or cases; level 2 requires real experimental results as a formal testing basis that can be evaluated separately, and the existing formal workflow establishes none of these conditions.
**Task**: T-completion
**Boundary & dispute notes**: Treating the possible experimental source of Materials Project structures as experimental results would confuse it with the source's task definition using DFT-computed properties for reward and evaluation; this judgment targets only the formal target labels and testing basis.
## R · Alignment with Experimental Needs

**Score**: 0; scored
**Criterion**: Data provides only idealized properties or proxy labels, without connection to a specific experimental use case. 
**Rationale**: The paper's formal objective is to compare RL algorithms optimizing DFT rewards, with property objectives set separately. It lists broad applications such as semiconductors and batteries, but does not define any target value as a specific experimental decision; the authors also explicitly do not claim the generated crystals are stable or easy to synthesize. Therefore neither fixed question is satisfied by the main benchmark.
**Level comparison**: Fixed question one: the paper lists potential applications, but the formal objective is DFT reward optimization, without defining a specific experimental use. Fixed question two: the authors explicitly do not guarantee stability or easy synthesis, and the candidate scope is not designed according to the key constraints of any experimental decision. Both questions are no, corresponding to 0; 1 requires the first question to be yes, and 2 requires both to be yes.
**Task**: T-completion
**Boundary & dispute notes**: Directly counting the target property's possible use in semiconductors or structural materials as the first fixed question holding might tend toward level 1; the source does not specify experiments to execute or select, so this judgment adopts level 0 and retains that boundary for the main Agent's review.
## C · Completeness of Key Experimental Conditions

**Score**: pending review; pending review
**Criterion**: Insufficient information; no numeric level selected for now
**Rationale**: The main task is virtual composition completion on a fixed lattice and DFT simulation evaluation. The paper lists computational software and parameters but does not define a corresponding physical experimental workflow; therefore which preparation, processing, and measurement conditions are necessary for this task cannot be determined, nor can the data itself be presumed missing based on the paper's non-disclosure of experimental conditions.
**Level comparison**: Level 0 needs confirming necessary experimental conditions are indeed missing; level 1 needs determining some key experimental conditions are given but items affecting interpretation are still missing; level 2 needs complete, traceable preparation, processing, and measurement conditions. Currently only computational conditions can be confirmed, and experimental-condition applicability and the necessary list cannot yet be established, so no numeric level is selected.
**Task**: T-completion
**Boundary & dispute notes**: Treating Appendix B.5's complete DFT settings as C=2 would confuse computational and experimental conditions; treating the paper's not writing physical experimental conditions as C=0 lacks basis for confirmed absence. Pending is retained.
## Limitations & Items Pending Review

- This report is a model assessment made per the current paper and frozen rubric, and does not represent expert certification.
- DFT success or failure cannot directly prove that generated crystals are synthesizable; the paper explicitly makes no stability or easy-synthesis claim.
- C's experimental-condition applicability and the list of conditions required by the task are not established by the current paper, so pending is retained.
- The titles and adjacent main text of Figure 1, Figure 2, Figure 6, and Tables 1-4 are used to locate the workflow and settings; this report's judgments do not rely on the internal visual structure of graphics, and no completion of image visual checking is claimed.
- PDF page 2 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 6 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 9 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 16 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 18 location hint: figure/table region not reliably detected; inner text may carry line numbers - verify against the line-numbered reading copy and figure/table labels
- PDF page 19 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 20 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 21 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 22 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages

## Score Revision Log

The review did not modify the initial scores.
