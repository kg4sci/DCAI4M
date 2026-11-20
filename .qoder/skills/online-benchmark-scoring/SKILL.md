---
name: online-benchmark-scoring
description: Incrementally score the materials-benchmark papers listed in the ONLINE Kingsoft Docs (金山文档 / kdocs) spreadsheet whose share URL is stored in the plain-text file `openxlsx` at the workspace root. Reads every sheet through the browser-use MCP (the doc is canvas-rendered and cannot be fetched over plain HTTP), decides which papers are already scored using a local registry, fetches full text via WebSearch/WebFetch when possible (falling back to the table fields), delegates scoring to the materials-benchmark-scoring rubric and its deterministic scripts, and writes local scored workbooks plus a consolidated summary. Use when the user asks to read/sync/score the online benchmark sheet, "openxlsx", the kdocs link, or to score only the not-yet-scored papers.
---

# Online Benchmark Sync & Score

Read the online kdocs workbook referenced by `openxlsx`, find papers that have **not** been scored yet, score them with the `materials-benchmark-scoring` rubric, and persist results **locally** (the online doc is left read-only).

- **Source of truth for the URL:** the plain-text file `openxlsx` in the workspace root (it contains one kdocs share URL).
- **Scored-state ledger:** `summary/scored_registry.json`, keyed by normalized `Paper ID / DOI` (or title when the DOI is empty). A paper is "scored" iff its key is present.
- **Scoring rules:** identical to `materials-benchmark-scoring` (X axis O/A/I/G/U/P + Y axis E/R/C). Reuse its scripts and [RUBRIC](../materials-benchmark-scoring/RUBRIC.md); do not re-derive the math by hand.
- **Outputs are local only:** `summary/raw/`, `summary/snapshot/`, `summary/scored/`, `summary/summary.md`. Never write back to the online doc.

## When to use

Trigger when the user asks any of:

- "Read the online sheet in `openxlsx` and score the papers that are not scored yet."
- "Sync the kdocs benchmark table and run the scoring on new rows."
- "Score the unscored benchmarks from the online doc."
- References the kdocs URL / `openxlsx` together with scoring, rating, or ranking.

## Prerequisites

- The **browser-use** MCP server (tools: `navigate_page`, `evaluate_script`, `list_pages`, `take_snapshot`). The kdocs grid is canvas-rendered, so `WebFetch` returns nothing useful; the browser is the only reliable reader.
- Python with `openpyxl` (`pip install openpyxl`).
- The sibling skill `materials-benchmark-scoring` (its `scripts/compute_scores.py` and `scripts/write_scores.py` are reused).

If the browser MCP is unavailable, or the doc sits behind a login that does not auto-resolve, **fall back**: ask the user to export the workbook to a local `.xlsx`, then run the same pipeline starting at Step 4 with that file as the snapshot (skip Steps 1-3).

## Output layout

```
summary/
  raw/<sheet>.json            # browser-extracted grid (name, header, rows)
  snapshot/<sheet>.xlsx       # local .xlsx mirror of each sheet (header row 1)
  scored/<sheet>.computed.json
  scored/<sheet>.scored.xlsx  # snapshot + appended score columns
  scored_registry.json        # ledger of already-scored papers
  summary.md                  # consolidated human-readable report
```

`<sheet>` is the sheet name with unsafe filename characters replaced by `_`.

## Workflow

Copy this checklist into the conversation and tick items as they complete:

```
- [ ] Step 0: Resolve the online URL from openxlsx
- [ ] Step 1: Open the doc in the browser and wait for load
- [ ] Step 2: List sheet names
- [ ] Step 3: Dump every sheet to summary/raw/*.json
- [ ] Step 4: Build local snapshots summary/snapshot/*.xlsx
- [ ] Step 5: Compute the unscored row list via the registry
- [ ] Step 6: Gather evidence per unscored row (full text, else table)
- [ ] Step 7: Score unscored rows (X + Y) and compute aggregates
- [ ] Step 8: Write scored workbooks and update the registry
- [ ] Step 9: Build the consolidated summary
- [ ] Step 10: Report
```

### Step 0: Resolve the online URL

Read the file `openxlsx` (plain text) at the workspace root and take the first line that starts with `http`. That is the kdocs share URL. Do not hard-code it.

### Step 1: Open the doc and wait for load

1. `list_pages`; if no usable page, `navigate_page` to the URL.
2. The URL may bounce through `account.wps.cn/...singlesso` and come back; that is normal. Wait until the sheet is ready:

   ```
   evaluate_script: () => new Promise(r => setTimeout(() => r(document.readyState + ' | ' + document.title), 4000))
   ```

   Expect `complete | <doc title>`. If the page still shows a hard login wall (no grid), stop and use the local-export fallback.

### Step 2: List sheet names

Read [scripts/js_get_sheet_names.js](scripts/js_get_sheet_names.js) and pass its content as the `function` argument of `evaluate_script` (no placeholder to fill). It returns the array of sheet names, e.g. `["性质预测（正向）","逆向设计","迭代优化（时序）"]`.

### Step 3: Dump every sheet

Only the **active** sheet's cells are resident in memory, so each tab must be activated (clicked) before it can be read. For each sheet name from Step 2:

1. Read [scripts/js_dump_sheet.js](scripts/js_dump_sheet.js).
2. Replace the placeholder `__SHEET_NAME__` with the actual sheet name.
3. Pass the resulting string as `function` to `evaluate_script`. The snippet clicks the tab, waits for the cells to load, then scans the used range with `getCellString(row, col)` (0-based) and returns `{name, header, rows}`.
4. Save the returned JSON to `summary/raw/<sheet>.json`.

**Preferred (large sheets):** a full grid is tens of KB, so do not round-trip it through the conversation. Start [scripts/local_receiver.py](scripts/local_receiver.py) in the background (`--port 8765 --outdir summary/raw`), then append to the dump snippet a `fetch('http://127.0.0.1:8765/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(obj)})` that posts the sheet object; the receiver writes `summary/raw/<sheet>.json` itself and the snippet returns only a tiny `{name, rows, http, ack}` confirmation. `http://127.0.0.1` is a trustworthy origin, so the https page may post to it; the receiver sends permissive CORS headers. Stop the receiver when done.

Clicking a tab that is already active is harmless, so run the snippet for every sheet including the first.

### Step 4: Build local snapshots

```
python .qoder/skills/online-benchmark-scoring/scripts/json_to_xlsx.py --many summary/raw --outdir summary/snapshot
```

This writes one `.xlsx` per sheet with the header on row 1, so the existing `read_benchmarks.py` / `write_scores.py` (1-based rows, header = row 1) line up.

### Step 5: Unscored row list

For each snapshot:

```
python .qoder/skills/online-benchmark-scoring/scripts/registry.py unscored \
    --snapshot summary/snapshot/<sheet>.xlsx \
    --registry summary/scored_registry.json \
    --id-col "Paper ID / DOI" --title-col "文献名称"
```

Prints a JSON array of `{row_index, paper_id, title}` for rows whose key is **not** in the registry. On first run (no registry) every data row is unscored. If a sheet uses different column names, adjust `--id-col` / `--title-col` to match its header.

### Step 6: Gather evidence per unscored row

For each unscored row, prefer full text over the table:

1. **Try full text.** Use `WebSearch` / `WebFetch` on the `Paper ID / DOI` and `文献名称`: arXiv (`arxiv.org/abs/...`), OpenReview, or the publisher page (DOI resolution). Extract the abstract + method/evaluation sections. Record `evidence_source = "fulltext"`.
2. **Fall back to the table.** If no full text is reachable, use the row's own fields (`文献名称`, `任务代码`, `输入/输出`, `模态类型`, `数据来源与 snapshot`, `体量`, `指标`, `Baseline`, `优点`, `备注`) as the evidence base. Record `evidence_source = "table"` and mark per-dimension confidence accordingly (usually `medium`/`low`).

Never invent content that appears in neither the full text nor the table.

### Step 7: Score and compute

Follow the `materials-benchmark-scoring` Step-3 rules exactly (read [RUBRIC.md](../materials-benchmark-scoring/RUBRIC.md)): evidence-only scoring, no terminology upgrades, claims vs demonstrations, scoring-time caps, per-dimension confidence, `NR`/`NA` for missing Y dimensions.

Build `summary/scored/<sheet>.scores.json` as a list of row objects in the [OUTPUT_FORMAT schema](../materials-benchmark-scoring/OUTPUT_FORMAT.md), **plus** two extra pass-through fields the registry needs: `"paper_id"` and `"title"`. Include **only unscored rows**.

Then run the deterministic aggregation (never do the arithmetic by hand):

```
python .qoder/skills/materials-benchmark-scoring/scripts/compute_scores.py \
    summary/scored/<sheet>.scores.json --out summary/scored/<sheet>.computed.json
```

### Step 8: Write scored workbooks + update registry

```
python .qoder/skills/materials-benchmark-scoring/scripts/write_scores.py \
    summary/snapshot/<sheet>.xlsx summary/scored/<sheet>.computed.json \
    --out summary/scored/<sheet>.scored.xlsx

python .qoder/skills/online-benchmark-scoring/scripts/registry.py add \
    --registry summary/scored_registry.json \
    --input summary/scored/<sheet>.computed.json \
    --sheet "<sheet name>"
```

`registry.py add` records each row's key with `scored_at`, `x5_final`, `level`, `y_total`, and `evidence_source`, so the next run skips it.

### Step 9: Consolidated summary

```
python .qoder/skills/online-benchmark-scoring/scripts/merge_summary.py \
    --scored-dir summary/scored --registry summary/scored_registry.json \
    --out summary/summary.md
```

### Step 10: Report

Print a compact table grouped by sheet:

| Sheet | Benchmark / title | X5 (final) | Level | Y total | Evidence | Caps |
|---|---|---:|---:|---:|---|---|

Then flag: rows scored from `table` only (lower confidence), rows with any `low` X confidence, rows with `y_complete = false`, and rows where a cap reduced `x5_final`. State how many rows were already scored (skipped) vs newly scored.

## Troubleshooting

- **Empty dump / all-empty rows for a sheet:** the tab click did not load it. Re-run the dump snippet for that sheet (it clicks again and waits). If still empty, increase the wait by re-running.
- **Login wall:** the view normally auto-resolves to read-only. If a hard sign-in blocks the grid, use the local-export fallback.
- **Sheet renamed / reordered:** names are read live in Step 2, so renames are handled; only the `--id-col`/`--title-col` headers are assumed stable.
- **`openpyxl` missing:** `pip install openpyxl`.
