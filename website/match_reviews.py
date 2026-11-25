"""Match 100 evaluation reports to datasets.json, inject agent_review scores, and copy reports to website."""
import json, os, re, difflib, shutil

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "论文测评报告_100篇", "论文测评报告_100篇")
DATASETS_PATH = os.path.join(os.path.dirname(__file__), "AI4M", "datasets.json")
REVIEWS_OUT = os.path.join(os.path.dirname(__file__), "AI4M", "reviews")

def extract_report_info(md_path):
    """Extract paper name, paper ID, and scores from a report markdown file."""
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    info = {}
    m = re.search(r'论文\s*ID\s*[：:]\s*(\S+)', text)
    info["paper_id"] = m.group(1) if m else ""

    m = re.search(r'论文名称\s*[：:]\s*(.+?)(?:\n|$)', text)
    info["paper_name"] = m.group(1).strip() if m else ""

    m = re.search(r'数据集[／/]基准\s*[：:]\s*(.+?)(?:\n|$)', text)
    info["dataset_benchmark"] = m.group(1).strip() if m else ""

    scores = {}
    dims = ["O", "A", "I", "G", "U", "P", "E", "R", "C"]
    for dim in dims:
        m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
        if m:
            final_val = m.group(3)
        else:
            m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
            final_val = m.group(1) if m else ""
        if final_val and final_val.replace(".", "").replace("待定", "").isdigit():
            try:
                scores[dim] = int(final_val)
            except ValueError:
                scores[dim] = final_val
        elif "待定" in final_val:
            cand = re.search(r'候选\s*(\d+)\s*分', final_val)
            scores[dim] = f"~{cand.group(1)}" if cand else "?"
        else:
            scores[dim] = final_val

    info["scores"] = scores
    info["text"] = text
    return info

def match_by_name(report_name, datasets):
    rn = report_name.lower().strip().rstrip(".")
    best_idx = None
    best_score = 0

    for i, ds in enumerate(datasets):
        dn = (ds.get("name", "") or "").lower().strip().rstrip(".")
        if rn == dn or rn in dn or dn in rn:
            return i
        ratio = difflib.SequenceMatcher(None, rn, dn).ratio()
        rn_words = set(re.findall(r'[a-z0-9]{3,}', rn))
        dn_words = set(re.findall(r'[a-z0-9]{3,}', dn))
        overlap = len(rn_words & dn_words) / max(len(rn_words), len(dn_words)) if rn_words and dn_words else 0
        score = ratio * 0.6 + overlap * 0.4
        if score > best_score:
            best_score = score
            best_idx = i

    return best_idx if best_score >= 0.55 else None

# ── Main ──

with open(DATASETS_PATH, "r", encoding="utf-8") as f:
    datasets = json.load(f)

# Clear and recreate reviews output directory
if os.path.exists(REVIEWS_OUT):
    shutil.rmtree(REVIEWS_OUT)
os.makedirs(REVIEWS_OUT, exist_ok=True)

matched = 0
unmatched = []
report_dirs = sorted(
    [d for d in os.listdir(REPORTS_DIR)
     if os.path.isdir(os.path.join(REPORTS_DIR, d))],
    key=str.lower
)

for dirname in report_dirs:
    md_path = os.path.join(REPORTS_DIR, dirname, "评分报告.md")
    if not os.path.exists(md_path):
        continue

    info = extract_report_info(md_path)
    report_name = info.get("paper_name", "") or dirname

    idx = match_by_name(report_name, datasets)
    if idx is not None:
        pid = info.get("paper_id", "")
        # Copy report to website/reviews/
        dest = os.path.join(REVIEWS_OUT, f"{pid}.md")
        # Write a cleaned-up version (without massive PDF line-number annotations)
        report_text = info["text"]
        shutil.copy2(md_path, dest)

        datasets[idx]["agent_review"] = {
            "paper_id": pid,
            "scores": info.get("scores", {}),
            "report_url": f"reviews/{pid}.md",
        }
        matched += 1
        print(f"  MATCHED: {report_name[:60]} → [{datasets[idx]['category']}] {datasets[idx]['name'][:60]}")
    else:
        unmatched.append(report_name)
        print(f"  UNMATCHED: {report_name[:80]}")

with open(DATASETS_PATH, "w", encoding="utf-8") as f:
    json.dump(datasets, f, ensure_ascii=False, indent=1)

print(f"\nMatched: {matched}/{len(report_dirs)}  |  Reports copied to AI4M/reviews/")
print(f"Unmatched: {len(unmatched)}")
for u in unmatched:
    print(f"  - {u[:100]}")