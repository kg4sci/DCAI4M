"""Convert browser-extracted kdocs sheet JSON into local .xlsx snapshots.

Usage:
    python json_to_xlsx.py <extracted.json> --out <snapshot.xlsx>
    python json_to_xlsx.py --many <dir_of_sheet_jsons> --outdir <dir>

Each extracted JSON is an object {"name", "header", "rows"} as produced by
scripts/js_dump_sheet.js. The output workbook puts the header on Excel row 1
and data rows below it, so read_benchmarks.py / write_scores.py (1-based rows,
header = row 1) stay aligned with the row_index values they emit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", (name or "").strip())
    return cleaned.strip("_") or "sheet"


def _load_objects(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    raise SystemExit(f"{path}: expected object or list of objects")


def _trim_trailing_empty(rows: list[list]) -> list[list]:
    rows = [list(r) for r in rows]
    while rows and all((c is None or str(c).strip() == "") for c in rows[-1]):
        rows.pop()
    return rows


def write_sheet(obj: dict, out: Path) -> int:
    rows = _trim_trailing_empty(obj.get("rows") or [])
    wb = Workbook()
    ws = wb.active
    ws.title = safe_name(obj.get("name"))[:31]
    for r in rows:
        ws.append(["" if c is None else c for c in r])
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return len(rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", nargs="?", help="single extracted JSON")
    p.add_argument("--out", help="output .xlsx (single mode)")
    p.add_argument("--many", help="directory of extracted JSONs")
    p.add_argument("--outdir", help="output directory (many mode)")
    args = p.parse_args()

    if args.many:
        if not args.outdir:
            raise SystemExit("--many requires --outdir")
        src = Path(args.many)
        dst = Path(args.outdir)
        dst.mkdir(parents=True, exist_ok=True)
        count = 0
        for f in sorted(src.glob("*.json")):
            for obj in _load_objects(f):
                out = dst / (safe_name(obj.get("name")) + ".xlsx")
                n = write_sheet(obj, out)
                print(f"{out}: {n} rows", file=sys.stderr)
                count += 1
        print(f"Wrote {count} snapshot workbook(s) to {dst}")
        return

    if not args.input or not args.out:
        raise SystemExit("single mode requires <input> and --out")
    objs = _load_objects(Path(args.input))
    if len(objs) != 1:
        raise SystemExit("single mode expects exactly one sheet object; use --many")
    n = write_sheet(objs[0], Path(args.out))
    print(f"Wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()
