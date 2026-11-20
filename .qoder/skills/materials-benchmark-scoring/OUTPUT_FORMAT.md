# Output Format

## Per-row JSON schema (input to `compute_scores.py`)

The agent produces a list of these objects and saves it as `scores.json`.

```json
{
  "row_index": 2,
  "benchmark_name": "string",
  "domain": "string (optional)",
  "task_summary": "string (one or two sentences)",
  "x_scores":   {"O": 0, "A": 0, "I": 0, "G": 0, "U": 0, "P": 0},
  "x_evidence": {
    "O": {"text": "quote or paraphrase", "confidence": "high|medium|low"},
    "A": {"text": "...", "confidence": "..."},
    "I": {"text": "...", "confidence": "..."},
    "G": {"text": "...", "confidence": "..."},
    "U": {"text": "...", "confidence": "..."},
    "P": {"text": "...", "confidence": "..."}
  },
  "y_scores":   {"E": 0, "R": 0, "C": 0},
  "y_evidence": {
    "E": {"text": "...", "confidence": "high|medium|low"},
    "R": {"text": "...", "confidence": "..."},
    "C": {"text": "...", "confidence": "..."}
  },
  "limitations": ["string", "..."],
  "overall_justification": "short paragraph"
}
```

Value rules:

- `row_index` is the 1-based Excel row number, matching the reader's output.
- Every `x_scores.*` is an integer 0-4.
- Every `y_scores.*` is an integer 0-2, or the string `"NR"` (not reported), or `"NA"` (not applicable).
- `evidence.text` is a short quote or paraphrase; use `"not reported"` verbatim when nothing supports the score.
- `evidence.confidence` is one of `"high"`, `"medium"`, `"low"`.

## Fields added by `compute_scores.py`

After running Step 4, each row additionally contains:

```json
{
  "x100_raw":     62.5,
  "x5_raw":       3.125,
  "x5_final":     2.5,
  "applied_caps": ["O<4 -> X5<=2.5"],
  "level":        2,
  "level_label":  "Design-oriented",
  "y_total":      4,
  "y_complete":   true
}
```

- `x5_final` is `x5_raw` after all numeric caps.
- `applied_caps` lists every cap that actually reduced `x5_final`, or the Level-5 demotion note if the gate failed.
- `y_total` is `null` when any Y dimension is `NR` or `NA`; `y_complete` is `false` in that case.

## Excel columns

`write_scores.py` appends these columns to the right of the original sheet, in this exact order. Existing cells are never modified.

| Column | Type | Source |
|---|---|---|
| `X_O` | int 0-4 | `x_scores.O` |
| `X_A` | int 0-4 | `x_scores.A` |
| `X_I` | int 0-4 | `x_scores.I` |
| `X_G` | int 0-4 | `x_scores.G` |
| `X_U` | int 0-4 | `x_scores.U` |
| `X_P` | int 0-4 | `x_scores.P` |
| `X100_raw` | float | `x100_raw` |
| `X5_raw` | float | `x5_raw` |
| `X5_final` | float | `x5_final` |
| `applied_caps` | string | `"; ".join(applied_caps)` |
| `level` | int 0-5 | `level` |
| `level_label` | string | `level_label` |
| `Y_E` | int 0-2 or `NR`/`NA` | `y_scores.E` |
| `Y_R` | int 0-2 or `NR`/`NA` | `y_scores.R` |
| `Y_C` | int 0-2 or `NR`/`NA` | `y_scores.C` |
| `Y_total` | int 0-6 or empty | `y_total` |
| `X_evidence_JSON` | string | JSON-encoded `x_evidence` |
| `Y_evidence_JSON` | string | JSON-encoded `y_evidence` |
| `limitations` | string | `"; ".join(limitations)` |
| `overall_justification` | string | `overall_justification` |

## Summary table for the user

After Step 5, print:

```
| Benchmark | X5 (final) | Level | Y total (0-6) | Caps applied |
|---|---:|---:|---:|---|
| ...   | ...        | ...   | ...           | ...          |
```

Then list:

- Rows with any `low` X confidence.
- Rows where `y_complete` is `false`.
- Rows where `applied_caps` is non-empty.
