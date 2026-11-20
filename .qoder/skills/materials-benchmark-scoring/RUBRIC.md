# Scoring Rubric (condensed from x.md and y.md)

Authoritative source: `x.md` (X axis) and `y.md` (Y axis) in the project root. This file is a compact, always-loaded reference. When in doubt, re-read the original files.

---

## X axis: Task Intelligence

Six dimensions, each an integer 0-4.

| Symbol | Dimension | Weight |
|---|---|---:|
| O | Output and Decision Role | 25% |
| A | Adaptivity and Sequentiality | 20% |
| I | Workflow Integration | 20% |
| G | Goal and Constraint Handling | 15% |
| U | Uncertainty and Failure Handling | 10% |
| P | Autonomy and Actionability | 10% |

### Dimension anchors

#### O - Output and Decision Role

| Score | Criterion |
|---:|---|
| 0 | No substantive ML task; only data processing or rule-based processing. |
| 1 | Single-property or single-label prediction. |
| 2 | Multi-property prediction, candidate ranking, or risk assessment. |
| 3 | Candidate generation, inverse design, or goal-directed design. |
| 4 | Decisions about the next candidates, experiments, resource allocation, or discovery strategy. |

#### A - Adaptivity and Sequentiality

| Score | Criterion |
|---:|---|
| 0 | Completely static, one-shot prediction. |
| 1 | Conditional prediction or generation without updating behavior based on new results. |
| 2 | One-time active selection. |
| 3 | Multi-round sequential optimization using simulation or offline feedback. |
| 4 | Multi-round, feedback-driven adaptive closed loop. |

#### I - Workflow Integration

| Score | Criterion |
|---:|---|
| 0 | No ML workflow. |
| 1 | A single model performing a single task. |
| 2 | An enhanced version of a single task. |
| 3 | Multiple models or modules connected in sequence. |
| 4 | Integrated discovery system connecting multiple stages (generation, prediction, screening, experiment planning, feedback updating). |

#### G - Goal and Constraint Handling

| Score | Criterion |
|---:|---|
| 0 | No explicit optimization objective or constraint. |
| 1 | A single optimization objective. |
| 2 | A single objective with static constraints. |
| 3 | Multi-objective or multi-constraint optimization. |
| 4 | Dynamic, multi-objective, resource-constrained decision-making. |

#### U - Uncertainty and Failure Handling

| Score | Criterion |
|---:|---|
| 0 | Deterministic outputs only. |
| 1 | Basic uncertainty reported but does not affect the strategy. |
| 2 | Uncertainty is used in candidate selection. |
| 3 | Noise, failures, and negative results are explicitly handled. |
| 4 | Uncertainty drives a risk-aware search strategy. |

#### P - Autonomy and Actionability

| Score | Criterion |
|---:|---|
| 0 | Outputs predictions only. |
| 1 | Provides recommendations; action rules are determined by humans. |
| 2 | Automatically executes a fixed workflow. |
| 3 | Automatically selects the next action based on feedback. |
| 4 | Autonomously plans, executes, monitors, and corrects the process. |

### Aggregation

```
X100 = 100 * [0.25*(O/4) + 0.20*(A/4) + 0.20*(I/4) + 0.15*(G/4) + 0.10*(U/4) + 0.10*(P/4)]
     = 6.25*O + 5*A + 5*I + 3.75*G + 2.5*U + 2.5*P
X5   = X100 / 20
```

### Mandatory caps

**Scoring-time restrictions** (apply before aggregation, by lowering the raw dimension score):

- **Cap 4.** If no agent or closed-loop process was actually implemented and executed, `P <= 1` and `A <= 1`.
- **Cap 5.** If a generative model is evaluated only by validity / novelty / diversity with no target properties, constraints, screening, or downstream decisions, `O <= 2`.
- **Cap 6.** If the paper claims feedback but never demonstrates that later decisions depend on earlier results, do not assign `A = 3` or `A = 4`.

**Post-aggregation caps** (applied by `compute_scores.py`; if several apply, the most restrictive wins):

- **Cap 1.** If `O < 4`, final `X5 <= 2.5`.
- **Cap 2.** If `A < 3`, final `X5 <= 3.0`.
- **Cap 3.** If `I < 3`, final `X5 <= 3.0`.
- **Cap 5 (numeric).** When Cap 5 fires at scoring time, additionally `X5 <= 2.5`.

### Level bands

| Final X5 | Level | Label |
|---|---:|---|
| 0 <= X5 < 0.5 | 0 | Data-level |
| 0.5 <= X5 < 1.5 | 1 | Predictive |
| 1.5 <= X5 < 2.5 | 2 | Design-oriented |
| 2.5 <= X5 < 3.75 | 3 | Decision-oriented |
| 3.75 <= X5 < 4.6 | 4 | Adaptive discovery |
| 4.6 <= X5 <= 5.0 | 5 | Autonomous discovery |

**Level 5 additional gate:** requires `O = 4 AND A >= 3 AND I = 4 AND P >= 3`. If the gate fails, demote to Level 4 and record `"Level 5 gate failed -> demoted to 4"` in `applied_caps`.

### Evidence and confidence

For every X dimension, record:

- `text`: a short quote or paraphrase from the row's content that justifies the score, or the string `"not reported"`.
- `confidence`: `high` (explicitly established), `medium` (supported but incomplete), `low` (limited or ambiguous, score is conservative).

---

## Y axis: Experimental Orientation

Three dimensions, each 0-2. The coarse 0-2 scale is intentional: it reduces subjective judgment for a literature review.

| Dimension | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| **E - Reliance on experimental results** | No actual experimental results; evaluation uses only simulations or proxy labels. | Experimental results are used for training, calibration, or a few illustrative cases, but do not constitute a formal experimental test. | Actual experimental results serve as a formal basis for testing; performance on the experimental data can be assessed separately. |
| **R - Alignment with experimental needs** | Data provide only idealized properties or proxy labels with no connection to a specific experimental use. | Data explicitly address one experimental need but do not cover the key constraints required to meet it. | Data and candidate scope support a clearly defined experimental decision and include the relevant objectives and key constraints (or ensure them by design). |
| **C - Completeness of key experimental conditions** | Only material identifiers and results are provided; conditions needed to interpret results are missing. | Some key conditions are provided, but omissions affect interpretation or comparison. | Key preparation, processing, and measurement conditions for the task are provided and traceable to samples or a standardized protocol. |

### E - Decision sequence

1. Are experimental results used at all? If no, `E = 0`.
2. Are they used only for training, calibration, or a few successful cases? If yes, `E = 1`.
3. Is there a defined experimental test set or predefined experimental evaluation, reported separately? If yes, `E = 2`.

Notes:

- Historical experimental measurements from literature or databases count as actual experimental results. Benchmark authors do not need to run new experiments.
- Simulation training + experimental testing can reach `E = 2`. Experimental training + simulation testing is typically `E = 1`.
- For mixed test sets, do not award `E = 2` if only an aggregate metric is reported and the experimental subset cannot be separated.

### R - Two fixed questions

1. Do the objectives represented in the data correspond to a clearly defined experimental use?
2. Do the data or candidate scope include the key constraints required for that use?

- Neither satisfied -> `R = 0`.
- Only (1) satisfied -> `R = 1`.
- Both satisfied -> `R = 2`.
- Insufficient information -> mark `NR`, do not guess.

Key constraints are determined by the benchmark's **stated intended use**, not by an exhaustive list. Multiple properties and closed-loop operation do not automatically earn additional points.

### C - Predefined key conditions per task

Typical key conditions to check:

| Task or property | Examples of key conditions |
|---|---|
| Battery performance | C-rate, voltage window, temperature, electrode information affecting the target metric. |
| Catalytic performance | Temperature, pressure or potential, reaction system, normalization method. |
| Mechanical performance | Processing / heat-treatment state, testing temperature, loading mode or strain rate. |
| Synthesis-condition recommendation | Precursors, proportions, temperature, time, atmosphere or solvent. |

Conditions fixed by a standardized protocol count as provided. If many records lack key conditions, do not award `C = 2` just because a few cases are complete.

### Avoiding double penalty across R and C

- **R** asks whether the data represent the practical problem to be solved.
- **C** asks whether the experimental context of the reported results is documented.

A dataset can score high on R and low on C, or the reverse.

### Aggregation

```
S = E + R + C   (range 0-6)
```

- Report the three component scores as the main result; the total is secondary.
- If any dimension is `NR`, do not compute `S` (leave it `null`); the script sets `y_complete = false`.
- `NA` is allowed when a dimension genuinely does not apply (e.g. a pure-simulation benchmark where `C = NA` while `E = 0`).
- Do not renormalize remaining dimensions when one is `NR` or `NA`; that would break comparability.

The total is the **experimental-orientation score of the data**. It is not an overall benchmark-quality score.

---

## Global evaluation principles (from x.md Section 2)

1. Use explicit evidence only.
2. Avoid terminology-based scoring.
3. Do not assume unreported capabilities.
4. Justify every score, or state "not reported".
5. Distinguish claims from demonstrations.
6. Evaluate tasks and behavior, not model size or accuracy.
7. Require actual integration for higher-level systems.
8. Require evidence of feedback for adaptive closed-loop classification.
