"""Consolidate per-sheet computed scores into a single human-readable report.

Usage:
    python merge_summary.py --scored-dir summary/scored \
        --registry summary/scored_registry.json --out summary/summary.md

Reads every <sheet>.computed.json under --scored-dir and joins each row with the
registry entry (by normalized paper_id/title) to add the evidence source. Emits
a markdown report grouped by sheet with the key metrics and a flags section.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def norm(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def key_for(paper_id, title) -> str:
    pid = norm(paper_id)
    if pid:
        return pid
    t = norm(title)
    return f"t:{t}" if t else ""


def _low_conf(row: dict) -> bool:
    for dim in (row.get("x_evidence") or {}).values():
        if isinstance(dim, dict) and str(dim.get("confidence", "")).lower() == "low":
            return True
    return False


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--scored-dir", required=True)
    p.add_argument("--registry", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    scored_dir = Path(args.scored_dir)
    reg_path = Path(args.registry)
    entries = {}
    if reg_path.exists():
        entries = json.loads(reg_path.read_text(encoding="utf-8")).get("entries", {})

    lines = ["# Online Benchmark Scoring Summary", ""]
    totals = {"rows": 0, "table_only": 0, "low_conf": 0, "incomplete_y": 0, "capped": 0}

    files = sorted(scored_dir.glob("*.computed.json"))
    if not files:
        lines.append("_No computed score files found yet._")
    for f in files:
        sheet = f.name.replace(".computed.json", "")
        rows = json.loads(f.read_text(encoding="utf-8"))
        lines.append(f"## Sheet: {sheet}")
        lines.append("")
        lines.append("| Row | Benchmark / title | X5 (final) | Level | Y total | Evidence | Caps |")
        lines.append("|---:|---|---:|---:|---:|---|---|")
        for r in rows:
            k = key_for(r.get("paper_id"), r.get("title") or r.get("benchmark_name"))
            reg = entries.get(k, {})
            evidence = r.get("evidence_source") or reg.get("evidence_source") or "?"
            caps = "; ".join(r.get("applied_caps") or []) or "-"
            name = r.get("title") or r.get("benchmark_name") or ""
            y = r.get("y_total")
            lines.append(
                f"| {r.get('row_index', '')} | {name} | {r.get('x5_final', '')} | "
                f"{r.get('level', '')} ({r.get('level_label', '')}) | {y if y is not None else 'NR/NA'} | "
                f"{evidence} | {caps} |"
            )
            totals["rows"] += 1
            if evidence == "table":
                totals["table_only"] += 1
            if _low_conf(r):
                totals["low_conf"] += 1
            if r.get("y_complete") is False:
                totals["incomplete_y"] += 1
            if r.get("applied_caps"):
                totals["capped"] += 1
        lines.append("")

    lines.append("## Flags")
    lines.append("")
    lines.append(f"- Total scored rows: {totals['rows']}")
    lines.append(f"- Scored from table only (lower confidence): {totals['table_only']}")
    lines.append(f"- Rows with any low X confidence: {totals['low_conf']}")
    lines.append(f"- Rows with incomplete Y (NR/NA): {totals['incomplete_y']}")
    lines.append(f"- Rows where a cap reduced X5: {totals['capped']}")
    lines.append("")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote summary to {out} ({totals['rows']} rows)")


if __name__ == "__main__":
    main()
