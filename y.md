# Data Scoring Framework

The scoring framework covers three dimensions:

1. **Reliance on experimental results:** Does benchmark evaluation rely on actual experimental results?
2. **Alignment with experimental needs:** Do the data support experimental decisions relevant to the intended application?
3. **Completeness of key experimental conditions:** Are the conditions necessary to interpret and use the experimental results provided?

A **three-level scale from 0 to 2** can be used. Compared with a 0–5 scale or a percentage score, this coarse-grained scale is more suitable for a literature review and can reduce subjective judgment.

| Dimension | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| **E: Reliance on experimental results** | No actual experimental results are used; evaluation relies entirely on simulations or other proxy labels. | Experimental results are used for training, calibration, or support through individual cases, but do not constitute a formal experimental test. | Actual experimental results serve as a formal basis for testing, and performance on the experimental data can be assessed separately. |
| **R: Alignment with experimental needs** | The data provide only idealized properties or proxy labels, without establishing their connection to specific experimental needs. | The data explicitly address an experimental need but do not cover the key constraints required to meet that need. | The data and candidate scope support a clearly defined experimental decision and include the relevant objectives and key constraints, or ensure through their design that these constraints are satisfied. |
| **C: Completeness of key experimental conditions** | Only material identifiers and results are provided; experimental conditions necessary to interpret the results are missing. | Some key conditions are provided, but omissions remain that affect interpretation or comparison. | The key preparation, processing, and measurement conditions required for the task are provided and can be traced to specific samples or a standardized experimental protocol. |

This table can serve as the main scoring rubric, but each dimension also requires a brief operational rule.

## E: Assess the Role of Experimental Results in Evaluation, Not Their Proportion in the Dataset

Historical experimental measurements reported in the literature or databases also count as actual experimental results. Benchmark authors do not need to conduct new experiments themselves.

Apply the following decision sequence:

- Are experimental results used? If not, assign **0**.
- Are experimental results used only for training, calibration, or demonstrating a few successful cases? Assign **1**.
- Is there a clearly defined experimental test set or a predefined experimental evaluation, with results reported separately? Assign **2**.

Therefore, **simulation-based training with experimental testing** can receive a score of 2, whereas **experimental training with simulation-based testing** typically receives a score of 1.

For test sets that mix simulated and experimental data, a full score should not be assigned if only an aggregate metric is reported and performance on the experimental subset cannot be determined.

Historical experimental testing and prospective testing through new experiments can be distinguished using separate labels; additional scoring levels are unnecessary.

This dimension measures the experimental basis of the evaluation. Test independence and statistical reliability should still be discussed in the evaluation-protocol section.

## R: Assess Whether the Data Support a Specific Experimental Decision

Do not use the number of properties as a substitute for alignment with experimental needs.

This dimension is the most susceptible to subjective judgment. Use two fixed questions:

> 1. Do the objectives represented in the data correspond to a clearly defined experimental use?
> 2. Do the data or candidate scope include the key constraints required for that use?

Assign scores as follows:

- If neither criterion can be established, assign **0**.
- If only the first criterion is satisfied, assign **1**.
- If both criteria are satisfied, assign **2**.
- If the available information is insufficient, mark the dimension as **not reported** rather than guessing.

Examples:

| Data setting | R assessment |
|---|---|
| The objective is solely to maximize or minimize a computed property, without specifying a corresponding experimental use. | Score 0 |
| Capacity labels are provided for screening battery materials, but operating conditions or feasibility information essential to that screening scenario are missing. | Score 1 |
| The data support capacity-based selection of the next batch of materials for testing within a clearly specified voltage window, C-rate, and candidate material scope. | Score 2 |

The **key constraints** must be determined according to the benchmark’s **stated intended use**. Do not require every study to address all possible factors, such as cost, toxicity, stability, and synthesizability.

For example, optimizing a single property within a set of materials already known to be preparable may fully match the experimental need and receive a score of 2.

Multiple properties and closed-loop operation do not automatically earn additional points.

## C: Use “Completeness of Key Conditions” Rather Than “Completeness of All Experimental Conditions”

Requiring complete experimental conditions is overly demanding and difficult to assess consistently.

A more practical approach is to **predefine a small set of essential conditions for each task, then check whether the data provide them**.

| Task or property | Examples of key conditions to check in advance |
|---|---|
| Battery performance | C-rate, voltage window, temperature, and electrode information that affects the target metric. |
| Catalytic performance | Temperature, pressure or potential, reaction system, and the method used to normalize performance. |
| Mechanical performance | Processing or heat-treatment state, testing temperature, and loading mode or strain rate. |
| Synthesis-condition recommendation | Precursors, proportions, temperature, time, and atmosphere or solvent. |

These are examples only. The specific checklist should be determined by the scope of the study.

Conditions explicitly specified in a standardized protocol should also count as **provided**; they do not need to be repeated in every data record.

If many records lack key conditions, the dataset should not receive a full score merely because a few cases are complete.

## Avoid Double Penalization Across R and C

The distinction is:

- **R assesses whether the data represent the practical problem that needs to be solved.**
- **C assesses whether the experimental context of the reported results is clearly documented.**

For example, a catalysis dataset that explicitly includes activity, selectivity, and stability objectives may receive a high R score. However, if measurement conditions are incompletely documented, its C score may still be low.

Conversely, detailed documentation of experimental conditions does not necessarily mean that the data cover the constraints required for the intended screening decision.

## Recommended Reporting Format

When compiling results, use a format such as the following for each study:

| Study | Training data source | Test data source | E | R | C | Scoring evidence |
|---|---|---|---:|---:|---:|---|
| Benchmark A | Simulation | Experiment | 2 | 1 | 2 | Relevant data description or supplementary material. |
| Benchmark B | Experiment | Experiment | 2 | 2 | 1 | Relevant data description or supplementary material. |

**Reporting the three component scores as the main result is more informative than reporting a single total score.**

If ranking is necessary, an equally weighted total can be used when information is available for all three dimensions:

S = E + R + C

The total ranges from **0 to 6**, and the component scores must still be retained.

The total should be called the **experimental-orientation score of the data**. It must not be interpreted as a measure of overall benchmark quality.

## Missing Information and Non-Applicable Dimensions

- Use **NR (not reported)** when information is insufficient, and do not calculate a total score.
- Use **NA (not applicable)** when a dimension genuinely does not apply.

For example, for a purely simulation-based benchmark with no experimental records, C may be marked as NA, while E = 0 indicates the absence of experimental measurement evidence.

Do not remove these dimensions and renormalize the remaining scores, as doing so would undermine comparability.