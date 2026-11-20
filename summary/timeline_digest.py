# -*- coding: utf-8 -*-
"""Build a compact year-sorted digest of the five dataset sheets (latest kdocs version).

Reads summary/raw/<sheet>.json (browser dump), drops bulky URL/bib columns,
normalizes header whitespace, and writes summary/timeline_digest.md plus
per-sheet year statistics for the timeline survey.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
SHEETS = ["预测与识别", "生成与逆向设计", "路线与步骤规划", "优化与实验推荐", "AI模型评测"]

KEEP = [
    "数据集名称／版本", "发布年份", "数据内容", "数据规模", "数据类型",
    "任务类型", "本阶段具体用途", "材料体系", "原始发布文献（DOI）",
    "代表性应用文献（DOI）", "基线模型（baseline）",
]


def norm(h: str) -> str:
    return re.sub(r"\s+", "", h or "")


def year_key(s: str) -> int:
    m = re.search(r"(19|20)\d{2}", s or "")
    return int(m.group(0)) if m else 9999


def clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def load(sheet: str) -> list[dict]:
    obj = json.loads((RAW / f"{sheet}.json").read_text(encoding="utf-8"))
    idx = {norm(h): i for i, h in enumerate(obj["header"])}
    out = []
    for row in obj["rows"][1:]:
        if not any((c or "").strip() for c in row):
            continue
        rec = {}
        for k in KEEP:
            i = idx.get(norm(k))
            rec[k] = (row[i] if i is not None and i < len(row) else "") or ""
        if not rec["数据集名称／版本"].strip():
            continue
        out.append(rec)
    out.sort(key=lambda r: (year_key(r["发布年份"]), r["数据集名称／版本"]))
    return out


def main() -> None:
    lines = ["# 数据集时间线摘要（最新版 kdocs，5 个任务 sheet）", ""]
    stats = []
    all_recs = []
    for sheet in SHEETS:
        recs = load(sheet)
        all_recs.extend(recs)
        tc = Counter((r["数据类型"] or "?").strip()[:1] for r in recs)
        print(sheet, "E/S/H:", dict(tc))
        years = [year_key(r["发布年份"]) for r in recs]
        known = [y for y in years if y != 9999]
        hist = {}
        for y in known:
            hist[y] = hist.get(y, 0) + 1
        hist_s = ", ".join(f"{y}:{n}" for y, n in sorted(hist.items()))
        stats.append((sheet, len(recs), min(known) if known else "-", max(known) if known else "-", hist_s))
        lines.append(f"## {sheet}（{len(recs)} 个数据集；年份分布 {hist_s}）")
        lines.append("")
        for r in recs:
            y = r["发布年份"].strip() or "年份不详"
            lines.append(f"### [{y}] {clip(r['数据集名称／版本'], 120)}")
            lines.append(f"- 任务类型: {clip(r['任务类型'], 120)} ｜ 数据类型: {clip(r['数据类型'], 100)} ｜ 材料体系: {clip(r['材料体系'], 120)}")
            lines.append(f"- 规模: {clip(r['数据规模'], 160)}")
            lines.append(f"- 内容: {clip(r['数据内容'], 400)}")
            lines.append(f"- 用途: {clip(r['本阶段具体用途'], 250)}")
            lines.append(f"- 原始文献: {clip(r['原始发布文献（DOI）'], 160)}")
            if r.get("基线模型（baseline）", "").strip():
                lines.append(f"- 基线: {clip(r['基线模型（baseline）'], 160)}")
            if r["代表性应用文献（DOI）"].strip():
                lines.append(f"- 应用文献: {clip(r['代表性应用文献（DOI）'], 160)}")
            lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("| sheet | 数据集数 | 最早 | 最晚 | 年份分布 |")
    lines.append("|---|---:|---:|---:|---|")
    for s in stats:
        lines.append("| " + " | ".join(str(x) for x in s) + " |")
    (ROOT / "timeline_digest.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"digest written: {ROOT / 'timeline_digest.md'}")
    for s in stats:
        print(s)
    gt = Counter((r["数据类型"] or "?").strip()[:1] for r in all_recs)
    uy = sum(1 for r in all_recs if year_key(r["发布年份"]) == 9999)
    print("TOTAL entries:", len(all_recs), "E/S/H:", dict(gt), "unknown_year:", uy)


if __name__ == "__main__":
    main()
