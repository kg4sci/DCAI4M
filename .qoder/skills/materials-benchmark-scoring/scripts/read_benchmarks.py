"""Read a materials-benchmark Excel file and dump rows as JSON.

Usage:
    python read_benchmarks.py <path> [--sheet NAME_OR_INDEX] [--header-row N]
                              [--out PATH | -]
                              [--preview]

Output (unless --preview): JSON array of {"row_index": int, "fields": {...}}.
row_index is the 1-based Excel row number so downstream scripts can align
scores with the original sheet.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import load_workbook


def _resolve_sheet(wb, sheet_arg: str | None):
    if sheet_arg is None:
        return wb.active
    # Allow 0-based index as string
    if sheet_arg.isdigit():
        idx = int(sheet_arg)
        if 0 <= idx < len(wb.sheetnames):
            return wb[wb.sheetnames[idx]]
        raise SystemExit(f"sheet index {idx} out of range; available: {wb.sheetnames}")
    if sheet_arg not in wb.sheetnames:
        raise SystemExit(f"sheet {sheet_arg!r} not found; available: {wb.sheetnames}")
    return wb[sheet_arg]


def _clean_header(cell, j: int) -> str:
    if cell is None:
        return f"col_{j + 1}"
    text = str(cell).strip()
    return text if text else f"col_{j + 1}"


def _is_empty_row(fields: dict) -> bool:
    for v in fields.values():
        if v is None:
            continue
        if isinstance(v, str) and not v.strip():
            continue
        return False
    return True


def read_rows(path: str, sheet: str | None, header_row: int) -> list[dict]:
    wb = load_workbook(path, data_only=True, read_only=True)
    ws = _resolve_sheet(wb, sheet)

    rows: list[dict] = []
    header: list[str] | None = None
    for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if i < header_row:
            continue
        if header is None:
            header = [_clean_header(c, j) for j, c in enumerate(row)]
            continue
        fields = {header[j]: (row[j] if j < len(row) else None) for j in range(len(header))}
        if _is_empty_row(fields):
            continue
        rows.append({"row_index": i, "fields": fields})

    wb.close()
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Path to .xlsx file")
    parser.add_argument("--sheet", default=None, help="Sheet name or 0-based index (default: active)")
    parser.add_argument("--header-row", type=int, default=1, help="1-based Excel row containing headers")
    parser.add_argument("--out", default="-", help="Output JSON path, or '-' for stdout")
    parser.add_argument("--preview", action="store_true", help="Print only column names and first two rows")
    args = parser.parse_args()

    if not Path(args.path).exists():
        raise SystemExit(f"file not found: {args.path}")

    rows = read_rows(args.path, args.sheet, args.header_row)

    if args.preview:
        cols = list(rows[0]["fields"].keys()) if rows else []
        preview = {
            "column_count": len(cols),
            "columns": cols,
            "row_count": len(rows),
            "first_rows": rows[:2],
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2, default=str))
        return

    text = json.dumps(rows, ensure_ascii=False, indent=2, default=str)
    if args.out == "-":
        sys.stdout.write(text + "\n")
    else:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {len(rows)} rows to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
