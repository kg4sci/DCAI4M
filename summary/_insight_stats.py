# -*- coding: utf-8 -*-
"""Cross-tabs for data-perspective insights: era x origin, reuse hubs, experimental ladder."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

RAW = Path("summary/raw")
SHEETS = ["预测与识别", "生成与逆向设计", "路线与步骤规划", "优化与实验推荐", "AI模型评测"]


def norm(h):
    return re.sub(r"\s+", "", h or "")


def year(s):
    m = re.search(r"(19|20)\d{2}", s or "")
    return int(m.group(0)) if m else None


def era(y):
    if y is None:
        return "?"
    if y <= 2010:
        return "P1 <=2010"
    if y <= 2016:
        return "P2 11-16"
    if y <= 2019:
        return "P3 17-19"
    if y <= 2022:
        return "P4 20-22"
    if y <= 2024:
        return "P5 23-24"
    return "P6 25-26"


def canon(name):
    n = re.split(r"[（(]", name)[0].strip().lower()
    exact = {"mp": "Materials Project"}
    if n in exact:
        return exact[n]
    for pre, key in [
        ("materials project", "Materials Project"), ("open catalyst 2020", "OC20"),
        ("oc20", "OC20"), ("moses", "MOSES"), ("gnome", "GNoME"), ("qmof", "QMOF"),
        ("omat24", "OMat24"), ("c2db", "C2DB"), ("icsd", "ICSD"), ("jarvis", "JARVIS"),
        ("hmof", "hMOF"), ("oqmd", "OQMD"), ("qm9", "QM9"), ("dismai", "Dismai-Bench"),
        ("metamatbench", "MetamatBench"),
    ]:
        if n.startswith(pre):
            return key
    return n


recs = []
for sh in SHEETS:
    obj = json.loads((RAW / f"{sh}.json").read_text(encoding="utf-8"))
    idx = {norm(h): i for i, h in enumerate(obj["header"])}
    for row in obj["rows"][1:]:
        if not any((c or "").strip() for c in row):
            continue
        get = lambda k: (row[idx[norm(k)]] if norm(k) in idx and idx[norm(k)] < len(row) else "") or ""
        name = get("数据集名称／版本").strip()
        if not name:
            continue
        recs.append(dict(sheet=sh, name=name, year=year(get("发布年份")),
                         typ=(get("数据类型").strip()[:1] or "?"), scale=get("数据规模")))

print("== era x origin ==")
ct = Counter((era(r["year"]), r["typ"]) for r in recs)
for e in ["P1 <=2010", "P2 11-16", "P3 17-19", "P4 20-22", "P5 23-24", "P6 25-26", "?"]:
    tot = sum(v for (ee, t), v in ct.items() if ee == e)
    print(e, "total", tot, {t: ct[(e, t)] for t in "ESH?" if ct[(e, t)]})

print("== reuse hubs (>=2 sheets) ==")
hub = defaultdict(set)
for r in recs:
    hub[canon(r["name"])].add(r["sheet"])
for k, v in sorted(hub.items(), key=lambda kv: -len(kv[1])):
    if len(v) >= 2:
        print(len(v), k, "|", "/".join(sorted(v)))
print("entries in >=2-sheet hubs:", sum(1 for r in recs if len(hub[canon(r["name"])]) >= 2))

print("== experimental (E) ladder ==")
for r in sorted((r for r in recs if r["typ"] == "E"), key=lambda r: r["year"] or 9999):
    print(r["year"], r["sheet"], r["name"][:34], "|", re.sub(r"\s+", " ", r["scale"])[:70])

print("== per-year origin (2011+) ==")
yc = Counter((r["year"], r["typ"]) for r in recs if r["year"] and r["year"] >= 2011)
for y in sorted({y for y, _ in yc}):
    print(y, {t: yc[(y, t)] for t in "ESH" if yc[(y, t)]})

print("== sheet x era ==")
sc = Counter((r["sheet"], era(r["year"])) for r in recs)
eras = ["P1 <=2010", "P2 11-16", "P3 17-19", "P4 20-22", "P5 23-24", "P6 25-26"]
for sh in SHEETS:
    print(sh, [sc[(sh, e)] for e in eras])

print("== evaluation sheet composition ==")
ev = [r for r in recs if r["sheet"] == "AI模型评测"]
print("total", len(ev), Counter(r["typ"] for r in ev))
for r in sorted(ev, key=lambda r: r["year"] or 9999):
    print(r["year"], r["typ"], r["name"][:40])
