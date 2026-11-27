# Single-Paper Dataset Scoring Report

## Score Summary

Reviewed dimensions use the reviewed scores from the Score Difference Review Table (.xlsx); other dimensions use the Agent scores.

| Dimension | Score | Source |
|---|---:|---|
| O · Output & Decision Role | 4 | Expert review |
| A · Adaptivity & Sequentiality | 3 | Expert review |
| I · Workflow Integration | 3 | Expert review |
| G · Goal & Constraint Handling | 3 | Expert review |
| U · Uncertainty & Failure Handling | 1 | Agent |
| P · Autonomy & Actionability | 3 | Expert review |
| E · Dependence on Experimental Results | 1 | Agent |
| R · Alignment with Experimental Needs | 2 | Agent |
| C · Completeness of Key Experimental Conditions | 1 | Agent |

## Agent Pending-Item Candidate Score Supplement

Below are the candidate scores the Agent added after the original review.

### O · candidate 4

**Criterion** Decisions about the next candidates, experiments, resource allocation, or discovery strategy. 

Provisionally proposed as 4, premised on this criterion allowing evaluation by the actual Output & Decision Role of a non-learning computational workflow. O-1 supports candidate generation, corresponding to level 3; O-2, O-3 further specify that the previous-round ranking determines which candidates receive longer next-round simulation, so it is closer to level 4 than level 3's generation-only, and also exceeds level 2's ranking output. The decision here is limited to subsequent computation objects, and O-4 specifies the experimental subset is still selected by researchers. On the other hand, O-5 describes geometric-rule assembly and O-6 describes GCMC simulation, from which a machine-learning task cannot be presumed; if level 0's machine-learning prerequisite takes precedence, the candidate will be affected. This applicability boundary is not yet clear, so a formal score cannot be formed.

**Source evidence**

- O-1 · [PDF page 1, main text lines 9-12](highlighted_paper.pdf#page=1)

  > computational approach to generate all conceivable MOFs from a given chemical library of building blocks (based on the
  > structures of known MOFs) and rapidly screen them to ﬁnd the best candidates for a speciﬁc application. From a library of
  > 102 building blocks we generated 137,953 hypothetical MOFs and for each one calculated the pore-size distribution,
  > surface area and methane-storage capacity. We identiﬁed over 300 MOFs with a predicted methane-storage capacity

- O-2 · [PDF page 3, right column lines 85-88](highlighted_paper.pdf#page=3)

  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- O-3 · [PDF page 4, full-width column lines 38-41](highlighted_paper.pdf#page=4)

  > Figure 4 | Adaptive three-stage screening to identify the best MOFs for methane storage. a, In the initial stage, ≏137,000 MOFs were screened for
  > methane storage at 35 bar through short simulations. b,c, The top 5% of the ﬁrst stage (b) and then the top 5% of the second stage (c), highlited in orange,
  > were recalculated using successively longer simulations, which signiﬁcantly reduced the statistical error each time. In a–c, MOFs are rank-ordered for their
  > methane adsorption abilities (best to worst runs from left to right), with statistical error indicated by purple bars. d,e, Perspective (d) and side (e) views of

- O-4 · [PDF page 5, left column lines 63-67](highlighted_paper.pdf#page=5)

  > promising predicted structures (for example, ≏300 here). Thus
  > chemical experience is still useful in choosing a smaller subset for
  > which experimental synthesis can be attempted, given constraints
  > of time, cost, available laboratory equipment and reagents, among
  > other criteria. Based on our own constraints, we found a predicted

- O-5 · [PDF page 2, main text lines 12-15](highlighted_paper.pdf#page=2)

  > mechanical) energy minimizations are involved; the pieces are
  > connected according to the geometric rules that govern how the
  > building blocks are connected in existing MOFs. The approach is
  > very much like snapping Tinkertoys or Lego bricks together.

- O-6 · [PDF page 2, main text lines 29-31](highlighted_paper.pdf#page=2)

  > (experimental, pseudo and pseudo after relaxation/optimization) we
  > predicted computationally the methane adsorption isotherms at
  > 298 K using grand canonical Monte Carlo (GCMC) simulations, as

**Still to verify**

- Need to clarify, when a non-machine-learning workflow has both candidate generation and sequential computational selection, whether the level-0 machine-learning prerequisite or the level-3/4 functional description takes precedence.

### I · candidate 3

**Criterion** Multiple models or modules connected in sequence. 

Provisionally proposed as 3, assuming the anchor's "modules" include geometric-rule generation and physical-simulation modules. I-1 connects generation, property computation, and screening into the same workflow, I-2 specifies GCMC computation, and I-3 specifies that previous-round results are used to select next-round simulation objects, supporting sequential connection of multiple modules. Another choice among the allowed anchors is 0: I-6 and I-2 show rule assembly and physical simulation, and whether they belong to the workflow recognized by this criterion still depends on the interpretation of the machine-learning prerequisite. I-4, I-5 also specify that experimental selection depends on personnel and the method does not provide a synthesis scheme, so it cannot be raised to level 4, which has been judged not met. The current evidence supports module connection but is insufficient to resolve the applicability conflict between 0 and 3.

**Source evidence**

- I-1 · [PDF page 1, main text lines 9-12](highlighted_paper.pdf#page=1)

  > computational approach to generate all conceivable MOFs from a given chemical library of building blocks (based on the
  > structures of known MOFs) and rapidly screen them to ﬁnd the best candidates for a speciﬁc application. From a library of
  > 102 building blocks we generated 137,953 hypothetical MOFs and for each one calculated the pore-size distribution,
  > surface area and methane-storage capacity. We identiﬁed over 300 MOFs with a predicted methane-storage capacity

- I-2 · [PDF page 2, main text lines 29-31](highlighted_paper.pdf#page=2)

  > (experimental, pseudo and pseudo after relaxation/optimization) we
  > predicted computationally the methane adsorption isotherms at
  > 298 K using grand canonical Monte Carlo (GCMC) simulations, as

- I-3 · [PDF page 3, right column lines 85-88](highlighted_paper.pdf#page=3)

  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- I-4 · [PDF page 5, left column lines 63-67](highlighted_paper.pdf#page=5)

  > promising predicted structures (for example, ≏300 here). Thus
  > chemical experience is still useful in choosing a smaller subset for
  > which experimental synthesis can be attempted, given constraints
  > of time, cost, available laboratory equipment and reagents, among
  > other criteria. Based on our own constraints, we found a predicted

- I-5 · [PDF page 6, left column lines 32-35](highlighted_paper.pdf#page=6)

  > screening strategy greatly accelerates its exploration. Our method
  > also does not provide, nor guarantee, a synthesis protocol for the
  > generated MOFs. Chemical intuition and synthesis experience are
  > still required to capitalize on the output from the computational

- I-6 · [PDF page 2, main text lines 12-15](highlighted_paper.pdf#page=2)

  > mechanical) energy minimizations are involved; the pieces are
  > connected according to the geometric rules that govern how the
  > building blocks are connected in existing MOFs. The approach is
  > very much like snapping Tinkertoys or Lego bricks together.

**Still to verify**

- Need to clarify whether I=3 covers pure rule-based generation, GCMC simulation, and screening modules, or whether the condition of an existing machine-learning workflow must first be met.

### C · candidate 1

**Criterion** Some key conditions are provided, but missing ones affect interpretation or comparison. 

Provisionally proposed as 1, holding only under the assumption that this criterion applies to the single-case experimental validation conditions used by the frozen task. The 35 bar, 298 K in the source around C-1 are whole-library computational screening conditions, and C-2's cycle count is also a computational setting; neither can replace experimental conditions. C-3 gives clues about NOTT-107's measured pressure and possible insufficient activation; C-4 gives its 298 K temperature and the illustrated excess-adsorption basis, and distinguishes PCN-14's 290 K experiment, so it is closer to level 1 than level 0's identifiers and results only. But this information covers only the control material and cannot be extrapolated to the 137,953 hypothetical structures; the current excerpt is also insufficient to verify whether sample activation, normalization, and protocol traceability are complete, so it cannot yet support level 2. C-5's statement that the generation method does not provide a synthesis protocol does not equal missing experimental records. The condition insufficiency is currently only pending verification, and the formal score remains limited by applicable scope and record completeness.

**Source evidence**

- C-1 · [PDF page 3, left column lines 78-80](highlighted_paper.pdf#page=3)

  > By attempting every combination of building blocks, subject to
  > the above constraints, 137,953 hypothetical MOF structures were
  > generated in total. We screened each MOF for methane storage at

- C-2 · [PDF page 3, right column lines 84-88](highlighted_paper.pdf#page=3)

  > online at hmofs.northwestern.edu). Screening occurred in three
  > stages: every MOF was subject to short 500-cycle GCMC simu-
  > lations, then the top 7,000 MOFs were subjected to 2,500 cycle
  > simulations and ﬁnally the top 350 from the second stage were
  > subjected to 12,500 cycle simulations (Fig. 4; a cycle consists of N

- C-3 · [PDF page 5, right column lines 86-92](highlighted_paper.pdf#page=5)

  > We observed in experimental measurements at Northwestern
  > University that NOTT-107 had a methane storage capacity ≏8%
  > lower at 35 bar than what had been predicted by our simulations.
  > This could be attributed partly to incomplete pore activation, which
  > is corroborated by a difference between the simulated Brunauer,
  > Emmet and Teller (BET) surface area51 (2,207 m2 g21) and the
  > measured BET surface area (1,770 m2 g21). The methane adsorption

- C-4 · [PDF page 6, left column lines 23-31](highlighted_paper.pdf#page=6)

  > Figure 6 | Comparison of experimental and simulated isotherms for
  > NOTT-107 and PCN 14. a,b, The organic ligand for NOTT-107 (a) is
  > structurally identical to that for PCN-14 (b) except that it bears four methyl
  > groups in the place of two fused aromatic rings. c, Comparison of excess
  > methane adsorption isotherms of NOTT-107 and PCN-14. All isotherm data
  > are at 298 K except experimental data for PCN-14 taken from ref. 40, which
  > was at 290 K. The simulations used the NOTT-107 structure generated by
  > our method (not optimized) and the PCN-14 structure determined
  > experimentally in ref. 40.

- C-5 · [PDF page 6, left column lines 32-36](highlighted_paper.pdf#page=6)

  > screening strategy greatly accelerates its exploration. Our method
  > also does not provide, nor guarantee, a synthesis protocol for the
  > generated MOFs. Chemical intuition and synthesis experience are
  > still required to capitalize on the output from the computational
  > generation and screening approach. In the future, it may be possible

**Still to verify**

- Need to clarify whether C applies in the frozen task dominated by simulated labels, and whether the NOTT-107 single-case validation record belongs to the evaluated dataset.
- Need to obtain the traceable preparation and pore-activation protocol for the specific NOTT-107 sample, and the adsorption-amount normalization and unit-conversion notes, to verify whether key conditions are complete, rather than presuming absence from the excerpt not listing them.

## Agent Original Review Record

The Agent scores using the same model in divided roles, adjudicated by an independent review and the main Agent.

- Paper ID: paper_819199dbc2b68f0b
- Paper title: Large-scale screening of hypothetical metal–organic frameworks
- Dataset / benchmark: Hypothetical MOF database
- Task: given a building-block library derived from synthesized MOFs, generating hypothetical structures by geometry and composition rules, and screening and ranking candidates in stages based on methane-storage computation results at 35 bar, 298 K.
- Evaluation object: the hypothetical metal-organic framework (MOF) dataset constructed in the paper and its methane-storage candidate generation and computational screening task: generating 137,953 hypothetical MOFs from 102 building blocks and screening storage capacity at 35 bar, 298 K; the NOTT-107 measurement is a single-case validation.
- Provided workflow: combining building blocks by known MOF connection geometry and imposing structural constraints to generate hypothetical MOFs; computing structural properties and methane adsorption; screening candidates with progressively lengthened GCMC simulations; researchers select NOTT-107 for experimental comparison.
- Model: gpt-6-sol
- Reasoning effort: high
- Agent report status: contains items pending review
- Highlighted paper: [open the line-numbered, evidence-highlighted PDF](highlighted_paper.pdf)

Source retrieval: 94 tool calls, 127 logical operations (sub-operations within batch requests counted separately).

Line-number note: each page starts at 1, numbered in reading order; text fragments in the same column and on the same baseline are merged. Detected repeated headers/footers, page numbers, and in-figure text are not numbered; columns are marked for two-column layouts. Line numbers are generated by this system, based on the line-numbered PDF reading copy, not the authors printed line numbers.

Evaluation object review: Re-checked the frozen object against the abstract, the formal screening definition on page 3, and the source of Figure 4 and Figure 6. The main object is indeed the 137,953 hypothetical MOFs generated from 102 building blocks and the computational screening for methane storage at 35 bar, 298 K; NOTT-107 is only a single-case measured validation, the structure-property trend belongs separately to T2, and future applications are not merged into T1. The frozen evaluation_object and evaluation_profile remain unchanged. The previous reply mistakenly used a simplified object; this time the frozen scope is restored.

Content excluded from this capability assessment: The output of structure-property correlation analysis is not conflated with the candidate-decision capability of the main screening task.; The single-case measured comparison of NOTT-107 is not treated as an experimental test set for the 137,953 candidates.; Human experimental-candidate selection based on time, cost, equipment, and reagents is not treated as automatic resource planning.; The iterative building-block design or carbon-capture, hydrogen-storage, and separation applications envisioned in the text are not counted as implemented tasks.

Fixed task: T1. Selection rationale: The abstract explicitly proposes generating hypothetical MOFs and rapidly screening application candidates; the "Systematic screening" section limits the main application and evaluation to high-pressure, room-temperature methane storage.

## Agent Initial Scoring, Independent Review & Adjudication

The independent review uses a fresh context of the same model, without the initial scores or expert scores; its opinion informs adjudication, not voting or averaging.

| Dimension | Initial | Independent review | Agent adjudication |
|---|---:|---:|---:|
| O | 4 | pending review | pending review |
| A | 3 | 3 | 3 |
| I | 3 | pending review | pending review |
| G | 3 | 3 | 3 |
| U | 1 | 3 | 1 |
| P | 3 | 3 | 3 |
| E | 1 | 1 | 1 |
| R | 2 | 1 | 2 |
| C | pending review | 1 | pending review |

Weighted total not computed: the original rubric did not specify the weight for O.

## O · Output & Decision Role

**Score** 4(Expert review)
**Criterion**: Insufficient information; no numeric level selected for now
**Rationale**: T1 outputs generated structures, ranks them, and decides the next round's computational objects based on simulation ranking; but the source's generation follows geometric rules, properties are computed by GCMC physical simulation, and no substantive machine learning task is established. The original O=0's machine learning premise and O=3/4's output and decision anchors are simultaneously relevant on this object, and the existing criterion cannot uniquely adjudicate.
**Level comparison**: O=2's candidate ranking, O=3's candidate generation, and O=4's next-round computational object allocation all have source facts; O=0 also explicitly states no substantive machine learning task and only rule-based processing. This paper's rule-based generation and GCMC simulation make the applicability boundary between 0 and higher levels impossible to resolve with the existing text, so the number is suspended.
**Task**: T1
**Boundary & dispute notes**: Initial 4 focuses on next-round computational resource allocation, while the Independent review's suspension focuses on non-learning implementation; each captures a different sentence meaning of the original anchor, so the suspension is accepted and neither 4 nor 0 is released.
## A · Adaptivity & Sequentiality

**Score** 3(Expert review)
**Criterion**: Multi-round sequential optimization using simulation or offline feedback. 
**Rationale**: After the whole library completes short GCMC simulations, the top 7,000 enter longer simulations; in the second round the top 350 again enter longer simulations. The two candidate updates directly depend on the previous round's simulation results, fitting multi-round sequential optimization with simulation feedback.
**Level comparison**: Level 0 static one-shot prediction, level 1 not updating behavior based on new results, and level 2 one-time screening are all insufficient to describe two consecutive selection updates based on simulated ranking. Level 3 explicitly accommodates multi-round sequential optimization with simulation feedback. Compared with level 4, this paper only gives a fixed three-stage recomputation procedure, without forming a complete closed loop where experimental results or new structure generation repeatedly enter the system and correct the strategy.
**Task**: T1
**Boundary & dispute notes**: "Adaptive three-stage" only describes two selection updates based on simulation results; the word "adaptive" alone cannot push it to level 4, but a preset number of rounds also cannot demote it to one-time screening.
## I · Workflow Integration

**Score** 3(Expert review)
**Criterion**: Insufficient information; no numeric level selected for now
**Rationale**: This paper connects building-block generation, GCMC property simulation, and three-level screening, but there is no evidence these stages are trained machine learning models. The original criterion I=0's "No ML workflow" and I=3's "Multiple models or modules connected in sequence" have an applicability boundary here, so Initial 3 cannot be directly retained.
**Level comparison**: The sequential connection of task stages fits I=3's "multiple models or modules"; I=4 still lacks automatic experiment planning and feedback. However, the original I=0 is "No ML workflow", and the implemented stages are not machine learning models. The original criterion does not explain whether such non-learning module chaining can be counted toward I=3.
**Task**: T1
**Boundary & dispute notes**: Initial 3 emphasizes the actual connection of generation, simulation, and screening modules; the Independent review's suspension points out that the full process is not an ML implementation, and the original level-0 premise cannot be ignored.
## G · Goal & Constraint Handling

**Score** 3(Expert review)
**Criterion**: Multi-objective or multi-constraint optimization. 
**Rationale**: The main objective is methane storage capacity; the formal generation algorithm separately limits the number of inorganic, organic, and functional-group types, and all formal candidates are generated under these constraints, belonging to multi-constraint optimization of the candidate decision space.
**Level comparison**: A single methane capacity objective plus separate caps for inorganic, organic, and functional-group categories exceeds level 2's single objective plus one static constraint, fitting level 3's "multi-constraint". Level 4 requires dynamic multi-objective decision-making with resource constraints; this paper leaves resource limits to researchers for experimental subset selection.
**Task**: T1
**Boundary & dispute notes**: These caps are indeed implemented before generating the 137,953 formal candidates and cannot be treated only as post-hoc cleaning; but they are all static construction constraints, insufficient to satisfy level-4 dynamic resource decision-making.
## U · Uncertainty & Failure Handling

**Score**: 1; scored
**Criterion**: Basic uncertainty reported but does not affect the strategy. 
**Rationale**: Figure 4 reports statistical error of simulation results and that longer simulations can reduce error; the top 5% are still selected by methane adsorption ranking. Page 1's swapping building blocks or connection points upon atomic overlap belongs to geometric validity checking in candidate generation, and cannot be upgraded to task-level handling of noise, negative results, or failures in formal screening.
**Level comparison**: Figure 4 explicitly shows simulated statistical error, satisfying level 1's basic uncertainty reporting; screening is based on capacity ranking, with no statistical error shown entering candidate selection decisions, so 2 is not taken. The retry for building-block assembly overlap belongs to geometric validity checking in the structure generation process, insufficient as level 3 task-level noise, failure, or negative-result handling; nor is there level 4 risk-aware search.
**Task**: T1
**Boundary & dispute notes**: Independent review 3 replaces building blocks or connection points based on atomic overlap; that mechanism only handles geometric conflicts in the generation step and cannot prove that candidate evaluation failures are retained and used in the strategy. Initial 1 relies on statistical error reporting and explicitly states it is not predictive uncertainty.
## P · Autonomy & Actionability

**Score** 3(Expert review)
**Criterion**: Automatically selects the next action based on feedback. 
**Rationale**: Within the fixed three-stage protocol, the system automatically determines the specific candidates for the next round's long simulations based on the previous round's methane storage simulation ranking. The experimental synthesis subset and actual resource arrangements are still decided by researchers.
**Level comparison**: The system not only automatically executes preset computational steps but also determines the next round's specific recomputation objects based on simulation ranking, fitting level 3's feedback-based selection of the next action. It does not autonomously conduct experiment planning, execution, monitoring, and error correction; human chemical experience and synthesis operations remain necessary, so 4 is not taken.
**Task**: T1
**Boundary & dispute notes**: A fixed number of rounds itself supports one aspect of level 2; but the capacity ranking after each run changes the specific computational objects of the next round, so 3 is chosen, limited to computational actions.
## E · Dependence on Experimental Results

**Score**: 1; scored
**Criterion**: Experimental results used for training, calibration, or few-shot examples, but do not constitute formal experimental testing. 
**Rationale**: The main 137,953 candidates are screened by simulated properties; the authors measure NOTT-107 and compare with simulated capacity, belonging to single-case experimental validation. Measured structures were used for input or structure checking, but Figure 2 notes no measured adsorption isotherms participate in its comparison.
**Level comparison**: Level 0's "no real experimental results" does not fit the NOTT-107 measurement; level 1 allows a few experimental examples, exactly corresponding to this paper's single-case comparison. Level 2 requires real experimental results as a formal testing basis and performance separately assessable on experimental data; Figure 2 uses measured structures as input but has no measured adsorption isotherms, and Figure 6 only gives a NOTT-107 versus literature PCN-14 comparison.
**Task**: T1
**Boundary & dispute notes**: E=2 cannot be judged solely from experimentally sourced structures, nor can E=0 be judged by ignoring the NOTT-107 measurement; real experiments are used only at the single-case validation level.
## R · Alignment with Experimental Needs

**Score**: 2; scored
**Criterion**: Data and candidate scope support a well-defined experimental decision, including relevant objectives and key constraints (or guaranteed by design). 
**Rationale**: Fixed question one: the data objective corresponds to finding MOFs for natural gas vehicles that can store methane at high density at 35 bar, 298 K, with a clear experimental use. Fixed question two: candidates are screened by storage capacity under these conditions, and the number of building-block types is limited, giving generated structures the reasonable synthesis complexity described in the paper. Both questions have source support; manual selection still requires resource judgment, and this step cannot be counted as automatic decision-making.
**Level comparison**: The original criterion fixes two questions: whether it explicitly targets a specific experimental need, yes; whether it covers key candidate constraints or design guarantees related to that need, yes, because building-block geometry and complexity caps take effect in generation. Level 1 requires missing key constraints; although there is no per-candidate synthesis protocol, the implemented candidate-scope constraints cannot be erased. Level 2 does not equal guaranteeing all candidates are synthesizable.
**Task**: T1
**Boundary & dispute notes**: Independent review 1 emphasizes the lack of a synthesis protocol; but the source explicitly implements a building-block complexity constraint and states these MOFs are reasonable synthesis targets. R=2 only recognizes that the candidate scope aligns with the experimental decision, and does not guarantee individual experimental success.
## C · Completeness of Key Experimental Conditions

**Score**: pending review; pending review
**Criterion**: Insufficient information; no numeric level selected for now
**Rationale**: The main database records hypothetical structures and simulated properties; a few experimental controls report pressure and temperature and note that NOTT-107 may have insufficient pore activation. The existing main text cannot determine whether the complete database has traceable sample-level experimental conditions, or how this metric should apply to records that are mainly simulated labels. Therefore non-disclosure is not directly judged as missing conditions, nor are GCMC cycle counts used to replace experimental conditions.
**Level comparison**: C=0 requires confirming that only material identity and results exist and necessary conditions are missing; Figure 6 and the main text at least report temperature and pressure for a single case, and the database is mainly simulation records, so a zero score cannot be inferred from non-disclosure. C=1 requires establishing partial conditions and confirming that missing ones affect interpretation or comparison; activation may affect results, but the full record scope is unclear. C=2 requires key preparation, processing, and measurement conditions traceable to samples or a unified protocol; the existing main text cannot verify whether the whole database satisfies this.
**Task**: T1
**Boundary & dispute notes**: The database cannot be deemed confirmed missing just because the paper does not write out the full preparation and activation steps, nor can GCMC cycle counts or a single figure caption replace evidence of the whole database's experimental-condition completeness.
## Limitations & Items Pending Review

- O and I are suspended because the boundary between the non-learning implementation and the original rubric's machine-learning premise is undecided, and cannot be released per the Initial scores.
- C lacks whole-database experimental-condition applicability and sample-level protocol coverage evidence, pending is retained; the single NOTT-107 case cannot replace whole-database conditions.
- U=1 uses only the basic-uncertainty interpretation of Monte Carlo statistical error, without extrapolating to predictive uncertainty or a risk strategy.
- This report is a model assessment made per the supplied paper and frozen rubric, not an expert-certification result.
- PDF page 4 Figure 4 has been visually inspected: a-c are respectively the simulated ranking plots of the full library, the top 7,000, and the top 350 MOFs; scoring evidence cites caption text, without interpreting graphic error bars as candidate-level predictive uncertainty.
- PDF page 6 Figure 6 has been visually inspected: c shows the simulated and experimental methane adsorption isotherms of NOTT-107 and PCN-14; the temperature difference is confirmed by the caption, and the two measured curves are not expanded into a whole-library experimental test set.
- PDF page 3 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 4 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 5 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages
- PDF page 6 location hint: Two-column reading order is heuristic; use page rendering for ambiguous passages

## Score Revision Log

- O: 4(scored) -> pending review (pending review). 
- A: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
- I: 3(scored) -> pending review (pending review). 
- G: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
- U: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
- P: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
- E: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
- R: score and status unchanged; revised the rationale, evidence, or other explanatory fields.
