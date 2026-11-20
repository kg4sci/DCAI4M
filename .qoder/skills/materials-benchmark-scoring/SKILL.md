---
name: materials-benchmark-scoring
description: Score materials-domain AI benchmarks stored in a user-specified Excel file (one benchmark per row) against the two-axis rubric defined by x.md and y.md. The X axis is task intelligence (six weighted dimensions O/A/I/G/U/P, each 0-4, aggregated to X5 in [0,5] with mandatory caps and a 0-5 level classification). The Y axis is experimental orientation (three dimensions E/R/C, each 0-2, summed to S in [0,6]). Use when the user asks to rate, score, evaluate, or rank a spreadsheet of materials benchmarks, or references x.md / y.md together with an .xlsx file.
---

# Materials Benchmark Scoring

Score every row of an Excel workbook against two rubrics and write the results back to a new workbook.

- **X axis (task intelligence):** 6 weighted dimensions `O / A / I / G / U / P`, each integer 0-4, aggregated to `X100` then `X5` in [0,5], then capped and mapped to a level 0-5. Defined in `x.md`, mirrored in [RUBRIC.md](RUBRIC.md).
- **Y axis (experimental orientation):** 3 dimensions `E / R / C`, each integer 0-2 (or `NR` / `NA`), summed to `S = E+R+C` in [0,6]. Defined in `y.md`, mirrored in [RUBRIC.md](RUBRIC.md).

## When to use

Trigger this skill when the user asks any of:

- "Score / rate / evaluate the benchmarks in this Excel."
- "Apply x.md and y.md to this survey spreadsheet."
- "Give each benchmark an intelligence score and an experimental-orientation score."
- Provides an `.xlsx` path where each row is one benchmark or one survey paper.

## Required inputs

Collect before starting. If any is missing, ask; do not guess.

| Input | Meaning | Default |
|---|---|---|
| `path` | Absolute path to the `.xlsx` file | required |
| `sheet` | Sheet name or 0-based index | active sheet |
| `name_col` | Column holding the benchmark / paper name | auto-detect |
| `content_cols` | Columns whose text is used as evidence (abstract, task description, dataset description, evaluation protocol, workflow, limitations, ...) | every non-name text column |
| `output_path` | Where to save the scored workbook | `<path>.scored.xlsx` |

## Workflow

Copy this checklist into the conversation and tick items as they complete:

```
- [ ] Step 1: Confirm inputs and inspect the workbook
- [ ] Step 2: Read rows to JSON
- [ ] Step 3: Score each row (X: 6 dims, Y: 3 dims) with evidence
- [ ] Step 4: Compute aggregates (X100, X5, caps, level, S) via script
- [ ] Step 5: Write scores back to a new Excel file
- [ ] Step 6: Report summary and flag low-confidence / NR rows
```

### Step 1: Confirm inputs and inspect the workbook

Run the reader with no `--out` to preview headers and the first two rows:

```
python scripts/read_benchmarks.py "<path>" --preview
```

Show the user the detected column names. Ask which column is the benchmark name and which columns should be treated as evidence text. Do not proceed until confirmed.

### Step 2: Read rows to JSON

```
python scripts/read_benchmarks.py "<path>" [--sheet <name>] --out rows.json
```

`rows.json` is a list of `{"row_index": <int>, "fields": {<col>: <value>, ...}}`. `row_index` is the 1-based Excel row number and is used later to align scores with the original sheet.

### Step 3: Score each row

For every entry in `rows.json`, produce one object with this shape:

```json
{
  "row_index": 2,
  "benchmark_name": "...",
  "task_summary": "...",
  "x_scores":   {"O": 0, "A": 0, "I": 0, "G": 0, "U": 0, "P": 0},
  "x_evidence": {"O": {"text": "...", "confidence": "high"}, "A": {"text": "...", "confidence": "medium"}, ...},
  "y_scores":   {"E": 0, "R": 0, "C": 0},
  "y_evidence": {"E": {"text": "...", "confidence": "high"}, "R": {"text": "..."}, "C": {"text": "..."}},
  "limitations": ["..."],
  "overall_justification": "..."
}
```

Rules (do not skip):

1. **Evidence only.** Assign a score only if the row's text explicitly supports it. If a capability is not documented, do not assume it exists.
2. **No terminology upgrades.** Words like "LLM", "agent", "autonomous", "closed-loop" do not by themselves raise a score. Look for implemented and evaluated behavior.
3. **Claims vs demonstrations.** Distinguish conceptual descriptions from what was actually run and reported.
4. **Score the task, not the paper.** Ignore writing quality, parameter count, and predictive accuracy.
5. **Per-dimension confidence.** Every X dimension and every Y dimension carries `high | medium | low`. If evidence is missing, mark Y as `NR` (not reported) or `NA` (not applicable) and keep the X score conservative (typically 0 or 1) with a note in `limitations`.
6. **Apply scoring-time caps from [RUBRIC.md](RUBRIC.md#mandatory-caps) before writing raw scores.** Specifically:
   - If no agent or closed-loop process was actually implemented and executed, cap `P <= 1` and `A <= 1`.
   - If a generative model is evaluated only by validity / novelty / diversity with no target properties, constraints, screening, or downstream decisions, cap `O <= 2`.
   - If the paper claims feedback but never shows that later decisions depend on earlier results, do not assign `A = 3` or `A = 4`.
7. **Numeric X5 caps** (`O<4 -> X5<=2.5`, `A<3 -> X5<=3.0`, `I<3 -> X5<=3.0`) are applied by the script in Step 4. Do not apply them by hand.

Save the list of row objects to `scores.json`.

### Step 4: Compute aggregates

Never do the arithmetic yourself. Run:

```
python scripts/compute_scores.py scores.json --out scores.computed.json
```

The script adds `x100_raw`, `x5_raw`, `x5_final`, `applied_caps`, `level`, `level_label`, `y_total`, and `y_complete` to every row. It also enforces the Level-5 gate (`O=4 AND A>=3 AND I=4 AND P>=3`) and demotes to Level 4 if the gate fails.

### Step 5: Write scores back to Excel

```
python scripts/write_scores.py "<path>" scores.computed.json --out "<output_path>" [--sheet <name>]
```

The script copies the original workbook and appends the columns listed in [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md#excel-columns). Existing cells are never overwritten.

### Step 6: Report

Print a compact summary table to the user:

| Benchmark | X5 (final) | Level | Y total (0-6) | Caps applied |
|---|---:|---:|---:|---|

Then flag:

- Rows with any `low` confidence on an X dimension.
- Rows with `NR` or `NA` on any Y dimension (their `y_total` will be `null`).
- Rows where a cap actually reduced `x5_final` below `x5_raw`.

Offer to write a short per-row justification paragraph if the user wants it in the paper.

## Additional resources

- Full rubric text, all dimension tables, mandatory caps, level bands: [RUBRIC.md](RUBRIC.md)
- JSON schema and Excel column layout: [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md)
- Utility scripts: `scripts/read_benchmarks.py`, `scripts/compute_scores.py`, `scripts/write_scores.py`
