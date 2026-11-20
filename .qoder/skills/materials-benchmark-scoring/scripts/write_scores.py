"""Merge scoring results back into a copy of the original Excel workbook.

Usage:
    python write_scores.py <original.xlsx> scores.computed.json
                           --out <output.xlsx>
                           [--sheet NAME_OR_INDEX]

The original workbook is preserved. Score columns are appended to the right of
the existing data. Rows are matched by `row_index` (1-based Excel row number).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openpyxl import load_workbook

EXTRA_COLS = [
    "X_O", "X_A", "X_I", "X_G", "X_U", "X_P",
    "X100_raw", "X5_raw", "X5_final", "applied_caps", "level", "level_label",
    "Y_E", "Y_R", "Y_C", "Y_total",
    "X_evidence_JSON", "Y_evidence_JSON",
    "limitations", "overall_justification",
]


def _resolve_sheet(wb, sheet_arg):
    if sheet_arg is None:
        return wb.active
    if sheet_arg.isdigit():
        idx = int(sheet_arg)
        if 0 <= idx < len(wb.sheetnames):
            return wb[wb.sheetnames[idx]]
        raise SystemExit(f"sheet index {idx} out of range; available: {wb.sheetnames}")
    if sheet_arg not in wb.sheetnames:
        raise SystemExit(f"sheet {sheet_arg!r} not found; available: {wb.sheetnames}")
    return wb[sheet_arg]


def _join_list(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def build_row_values(s: dict) -> list:
    xs = s.get("x_scores", {}) or {}
    ys = s.get("y_scores", {}) or {}
    return [
        xs.get("O"), xs.get("A"), xs.get("I"), xs.get("G"), xs.get("U"), xs.get("P"),
        s.get("x100_raw"), s.get("x5_raw"), s.get("x5_final"),
        _join_list(s.get("applied_caps")), s.get("level"), s.get("level_label"),
        ys.get("E"), ys.get("R"), ys.get("C"), s.get("y_total"),
        json.dumps(s.get("x_evidence", {}), ensure_ascii=False),
        json.dumps(s.get("y_evidence", {}), ensure_ascii=False),
        _join_list(s.get("limitations")),
        s.get("overall_justification", "") or "",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("xlsx", help="original workbook")
    parser.add_argument("scores_json", help="scores.computed.json")
    parser.add_argument("--sheet", default=None, help="sheet name or 0-based index (default: active)")
    parser.add_argument("--out", required=True, help="output workbook path")
    args = parser.parse_args()

    if not Path(args.xlsx).exists():
        raise SystemExit(f"workbook not found: {args.xlsx}")

    scores = json.loads(Path(args.scores_json).read_text(encoding="utf-8"))
    if not isinstance(scores, list):
        raise SystemExit("scores.json must be a list")

    by_row: dict[int, dict] = {}
    for s in scores:
        idx = s.get("row_index")
        if idx is None:
            raise SystemExit("every score object must have a row_index")
        by_row[int(idx)] = s

    wb = load_workbook(args.xlsx)
    ws = _resolve_sheet(wb, args.sheet)

    start_col = ws.max_column + 1
    for j, name in enumerate(EXTRA_COLS):
        ws.cell(row=1, column=start_col + j, value=name)

    written = 0
    for row_idx, s in by_row.items():
        values = build_row_values(s)
        for j, v in enumerate(values):
            ws.cell(row=row_idx, column=start_col + j, value=v)
        written += 1

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.out)
    print(f"Wrote {written} scored rows to {args.out}")


if __name__ == "__main__":
    main()
