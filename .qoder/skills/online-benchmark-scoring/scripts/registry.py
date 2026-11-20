"""Local ledger of which papers have already been scored.

The online kdocs sheet carries no score columns, so "already scored" is tracked
locally in a registry JSON keyed by a normalized Paper ID / DOI (or the title
when the DOI cell is empty).

Usage:
    python registry.py unscored --snapshot <sheet.xlsx> --registry <reg.json> \
        [--id-col "Paper ID / DOI"] [--title-col "文献名称"]
    python registry.py add --registry <reg.json> --input <scores.computed.json> \
        --sheet "<sheet name>" [--source fulltext|table]
    python registry.py show --registry <reg.json>

`unscored` prints a JSON array of {"row_index","paper_id","title"} for data rows
whose key is absent from the registry (row_index is the 1-based Excel row).
`add` records one entry per scored row, reading paper_id/title from the score
objects (pass-through fields) and the computed aggregates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import load_workbook


def norm(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def key_for(paper_id, title) -> str:
    pid = norm(paper_id)
    if pid:
        return pid
    t = norm(title)
    return f"t:{t}" if t else ""


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "entries": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("version", 1)
    data.setdefault("entries", {})
    return data


def save_registry(path: Path, reg: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


def _header_index(ws, want: str):
    for cell in ws[1]:
        if str(cell.value or "").strip() == want:
            return cell.column - 1
    return None


def cmd_unscored(args) -> None:
    reg = load_registry(Path(args.registry))
    entries = reg["entries"]
    wb = load_workbook(args.snapshot, data_only=True, read_only=True)
    ws = wb.active
    icol = _header_index(ws, args.id_col)
    tcol = _header_index(ws, args.title_col)
    if icol is None and tcol is None:
        raise SystemExit(f"neither {args.id_col!r} nor {args.title_col!r} found in header")
    out = []
    for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if i == 1:
            continue
        pid = row[icol] if icol is not None and icol < len(row) else None
        title = row[tcol] if tcol is not None and tcol < len(row) else None
        if not (pid and str(pid).strip()) and not (title and str(title).strip()):
            continue  # blank row
        k = key_for(pid, title)
        if k and k not in entries:
            out.append({"row_index": i, "paper_id": str(pid or "").strip(), "title": str(title or "").strip()})
    wb.close()
    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")


def cmd_add(args) -> None:
    reg = load_registry(Path(args.registry))
    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("input must be a list of score objects")
    now = datetime.now(timezone.utc).isoformat()
    added = 0
    for s in rows:
        pid = s.get("paper_id") or ""
        title = s.get("title") or s.get("benchmark_name") or ""
        k = key_for(pid, title)
        if not k:
            continue
        reg["entries"][k] = {
            "sheet": args.sheet,
            "paper_id": str(pid).strip(),
            "title": str(title).strip(),
            "row_index": s.get("row_index"),
            "scored_at": now,
            "x5_final": s.get("x5_final"),
            "level": s.get("level"),
            "level_label": s.get("level_label"),
            "y_total": s.get("y_total"),
            "evidence_source": s.get("evidence_source") or args.source,
        }
        added += 1
    save_registry(Path(args.registry), reg)
    print(f"Recorded {added} scored entr(ies); registry now has {len(reg['entries'])}")


def cmd_show(args) -> None:
    reg = load_registry(Path(args.registry))
    per_sheet = {}
    for e in reg["entries"].values():
        per_sheet.setdefault(e.get("sheet", "?"), 0)
        per_sheet[e.get("sheet", "?")] += 1
    print(json.dumps({"total": len(reg["entries"]), "per_sheet": per_sheet}, ensure_ascii=False, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("unscored")
    u.add_argument("--snapshot", required=True)
    u.add_argument("--registry", required=True)
    u.add_argument("--id-col", default="Paper ID / DOI")
    u.add_argument("--title-col", default="文献名称")
    u.set_defaults(fn=cmd_unscored)

    a = sub.add_parser("add")
    a.add_argument("--registry", required=True)
    a.add_argument("--input", required=True)
    a.add_argument("--sheet", required=True)
    a.add_argument("--source", default=None, help="default evidence_source if rows lack one")
    a.set_defaults(fn=cmd_add)

    s = sub.add_parser("show")
    s.add_argument("--registry", required=True)
    s.set_defaults(fn=cmd_show)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
