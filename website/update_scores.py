"""Update datasets.json with new scores from 数据集最终评分总表.xlsx and updated reports from zip."""
import json, os, re, shutil, difflib

XLSX_PATH = os.path.join(os.path.dirname(__file__), "..", "数据集最终评分总表.xlsx")
NEW_REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "论文测评报告_100篇_更新评分", "论文测评报告_100篇")
DATASETS_PATH = os.path.join(os.path.dirname(__file__), "AI4M", "datasets.json")
REVIEWS_OUT = os.path.join(os.path.dirname(__file__), "AI4M", "reviews")

X_DIMS = ["O", "A", "I", "G", "U", "P"]
Y_DIMS = ["E", "R", "C"]
ALL_DIMS = X_DIMS + Y_DIMS

# ── Part 1: Parse master score table ──

import openpyxl
wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
ws = wb["数据集总表"]

# Column mapping from header row 9:
# Col 1=类别, 2=Paper name, 3=Paper ID
# Cols 4-21: X-axis (O A I G U P), each 3 cols (Agent/Expert/Final)
# Cols 22-30: Y-axis (E R C), each 3 cols (Agent/Expert/Final)
# Col mapping by dimension:
col_map = {}
base = 4  # O starts at col 4
for dim in X_DIMS:
    col_map[dim] = {"agent": base, "expert": base+1, "final": base+2}
    base += 3
for dim in Y_DIMS:
    col_map[dim] = {"agent": base, "expert": base+1, "final": base+2}
    base += 3

master = {}  # paper_id -> {category, name, agent_scores, expert_scores, final_scores}
for row_idx in range(10, ws.max_row + 1):
    pid = str(ws.cell(row_idx, 3).value or "").strip()
    if not pid or pid == "None":
        continue
    cat = str(ws.cell(row_idx, 1).value or "").strip()
    name = str(ws.cell(row_idx, 2).value or "").strip()

    agent_scores = {}
    expert_scores = {}
    final_scores = {}
    for dim in ALL_DIMS:
        cm = col_map[dim]
        agent_scores[dim] = ws.cell(row_idx, cm["agent"]).value
        expert_scores[dim] = ws.cell(row_idx, cm["expert"]).value
        final_scores[dim] = ws.cell(row_idx, cm["final"]).value

    master[pid] = {
        "category": cat,
        "name": name,
        "agent_scores": agent_scores,
        "expert_scores": expert_scores,
        "final_scores": final_scores,
    }

print(f"Master table: {len(master)} entries")

# ── Part 2: Extract updated agent reviews from new reports ──

def extract_report_info(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    info = {}
    m = re.search(r'论文\s*ID\s*[：:]\s*(\S+)', text)
    info["paper_id"] = m.group(1) if m else ""
    m = re.search(r'论文名称\s*[：:]\s*(.+?)(?:\n|$)', text)
    info["paper_name"] = m.group(1).strip() if m else ""

    scores = {}
    for dim in ALL_DIMS:
        m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
        if m:
            final_val = m.group(3)
        else:
            m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
            final_val = m.group(1) if m else ""
        if final_val and re.match(r'^\d+$', final_val):
            scores[dim] = int(final_val)
        elif "待定" in final_val:
            cand = re.search(r'候选\s*(\d+)\s*分', final_val)
            scores[dim] = f"~{cand.group(1)}" if cand else "?"
        else:
            scores[dim] = final_val
    info["scores"] = scores
    info["text"] = text
    return info

# ── Trim function for reports ──
def trim_report(text):
    lines = text.split('\n')
    out = []
    in_evidence = False
    for line in lines:
        if re.match(r'^## (初评|独立审查|最终裁决|[OAIUGPERC] ·)', line):
            in_evidence = True
            out.append(line)
            out.append('')
            continue
        if in_evidence:
            if re.match(r'^## (评分修订记录|局限与待复核)', line):
                in_evidence = False
                out.append(line)
                continue
            if re.match(r'^## (?!.*证据)', line) and not re.match(r'^###', line):
                in_evidence = False
                out.append(line)
                continue
            if re.match(r'^(\*\*评分\*\*|\*\*对应标准\*\*|\*\*判定理由\*\*|\*\*分档比较\*\*|\*\*任务归属\*\*|\*\*边界)', line):
                out.append(line)
                continue
            continue
        out.append(line)
    return '\n'.join(out)

# ── Main: match, copy, update ──

with open(DATASETS_PATH, "r", encoding="utf-8") as f:
    datasets = json.load(f)

# Clear and recreate reviews dir
if os.path.exists(REVIEWS_OUT):
    shutil.rmtree(REVIEWS_OUT)
os.makedirs(REVIEWS_OUT, exist_ok=True)

report_dirs = sorted(
    [d for d in os.listdir(NEW_REPORTS_DIR)
     if os.path.isdir(os.path.join(NEW_REPORTS_DIR, d))],
    key=str.lower
)

agent_updated = 0
score_updated = 0
expert_added = 0

# Build paper_id -> dataset index mapping using matching
# First try by paper_id from reports, then by paper_id from master table
pid_to_ds = {}  # from reports
name_to_ds = {}  # for fuzzy matching fallback

for i, ds in enumerate(datasets):
    dn = (ds.get("name", "") or "").lower().strip().rstrip(".")
    name_to_ds[dn] = i

for dirname in report_dirs:
    md_path = os.path.join(NEW_REPORTS_DIR, dirname, "评分报告.md")
    if not os.path.exists(md_path):
        continue

    info = extract_report_info(md_path)
    pid = info.get("paper_id", "")

    # Try direct pid match from master table
    if pid in master:
        master_entry = master[pid]
        paper_name = master_entry["name"]
    else:
        # Fall back to fuzzy match
        paper_name = info.get("paper_name", "") or dirname

    # Find dataset index
    idx = None
    # Match by paper_id from master
    for i, ds in enumerate(datasets):
        ar = ds.get("agent_review", {})
        if ar.get("paper_id") == pid:
            idx = i
            break

    if idx is None:
        # Fuzzy match by name
        rn = paper_name.lower().strip().rstrip(".")
        best_score = 0
        for dn, di in name_to_ds.items():
            if rn == dn or rn in dn or dn in rn:
                idx = di
                break
            ratio = difflib.SequenceMatcher(None, rn, dn).ratio()
            rn_words = set(re.findall(r'[a-z0-9]{3,}', rn))
            dn_words = set(re.findall(r'[a-z0-9]{3,}', dn))
            overlap = len(rn_words & dn_words) / max(len(rn_words), len(dn_words)) if rn_words and dn_words else 0
            score = ratio * 0.6 + overlap * 0.4
            if score > best_score:
                best_score = score
                idx = di
        if best_score < 0.55:
            idx = None

    if idx is None:
        print(f"  SKIP: {paper_name[:60]} — no match in datasets.json")
        continue

    ds = datasets[idx]

    # ── Update agent_review scores from master table ──
    if pid in master:
        me = master[pid]
        agent_scores = {}
        for dim in ALL_DIMS:
            v = me["agent_scores"][dim]
            if v is not None and isinstance(v, (int, float)):
                agent_scores[dim] = int(v) if v == int(v) else v
            else:
                agent_scores[dim] = v
        datasets[idx]["agent_review"] = {
            "paper_id": pid,
            "scores": agent_scores,
            "report_url": f"reviews/{pid}.md",
        }
        agent_updated += 1

        # ── Add expert_review ──
        expert_scores = {}
        for dim in ALL_DIMS:
            v = me["expert_scores"][dim]
            if v is not None and isinstance(v, (int, float)):
                expert_scores[dim] = int(v) if v == int(v) else v
            else:
                expert_scores[dim] = v
        datasets[idx]["expert_review"] = {
            "paper_id": pid,
            "scores": expert_scores,
        }
        expert_added += 1

        # ── Update overall score from final_scores average ──
        total = 0
        count = 0
        for dim in ALL_DIMS:
            v = me["final_scores"][dim]
            if v is not None and isinstance(v, (int, float)):
                total += float(v)
                count += 1
        if count > 0:
            datasets[idx]["score"] = round(total / count, 1)
            score_updated += 1

    # ── Copy trimmed report to website ──
    if pid:
        dest = os.path.join(REVIEWS_OUT, f"{pid}.md")
        trimmed = trim_report(info["text"])
        with open(dest, "w", encoding="utf-8") as f:
            f.write(trimmed)

    print(f"  UPDATED: [{ds.get('category','')}] {ds['name'][:50]}")

# ── Write back ──
with open(DATASETS_PATH, "w", encoding="utf-8") as f:
    json.dump(datasets, f, ensure_ascii=False, indent=1)

print(f"\nAgent reviews updated: {agent_updated}")
print(f"Expert reviews added: {expert_added}")
print(f"Overall scores updated: {score_updated}")
print(f"Reports copied: {len(report_dirs)}")