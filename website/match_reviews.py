"""Match 100 evaluation reports to datasets.json and inject agent_review scores."""
import json, os, re, difflib

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "论文测评报告_100篇", "论文测评报告_100篇")
DATASETS_PATH = os.path.join(os.path.dirname(__file__), "AI4M", "datasets.json")

def extract_report_info(md_path):
    """Extract paper name, paper ID, and scores from a report markdown file."""
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    info = {}
    # Paper ID
    m = re.search(r'论文\s*ID\s*[：:]\s*(\S+)', text)
    info["paper_id"] = m.group(1) if m else ""

    # Paper name
    m = re.search(r'论文名称\s*[：:]\s*(.+?)(?:\n|$)', text)
    info["paper_name"] = m.group(1).strip() if m else ""

    # Dataset name
    m = re.search(r'数据集[／/]基准\s*[：:]\s*(.+?)(?:\n|$)', text)
    info["dataset_benchmark"] = m.group(1).strip() if m else ""

    # Extract scores from the summary table (表 with O/A/I/G/U/P/E/R/C)
    # Find the summary scores table
    scores = {}
    # Pattern: | O | 3 | 3 | 3 |  -> takes the last (final) score
    dims = ["O", "A", "I", "G", "U", "P", "E", "R", "C"]
    for dim in dims:
        # Try the 4-column format: | O | 3 | 3 | 3 |
        m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
        if m:
            final_val = m.group(3)
        else:
            # Try 2-column format: | O | 3 |
            m = re.search(rf'^\|\s*{dim}\s*\|\s*(\S+)\s*\|', text, re.MULTILINE)
            final_val = m.group(1) if m else ""
        if final_val and final_val.replace(".", "").replace("待定", "").isdigit():
            try:
                scores[dim] = int(final_val)
            except ValueError:
                scores[dim] = final_val  # keep as string for "待定"
        elif "待定" in final_val:
            # Extract candidate score
            cand = re.search(r'候选\s*(\d+)\s*分', final_val)
            scores[dim] = f"~{cand.group(1)}" if cand else "?"
        else:
            scores[dim] = final_val

    info["scores"] = scores
    return info

def match_by_name(report_name, datasets):
    """Match a report paper name to a dataset entry. Returns (index, score) or None."""
    rn = report_name.lower().strip().rstrip(".")

    best_idx = None
    best_score = 0

    for i, ds in enumerate(datasets):
        dn = (ds.get("name", "") or "").lower().strip().rstrip(".")

        # Exact match
        if rn == dn or rn in dn or dn in rn:
            return i

        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, rn, dn).ratio()
        # Also try matching first N meaningful words
        rn_words = set(re.findall(r'[a-z0-9]{3,}', rn))
        dn_words = set(re.findall(r'[a-z0-9]{3,}', dn))
        if rn_words and dn_words:
            overlap = len(rn_words & dn_words) / max(len(rn_words), len(dn_words))
        else:
            overlap = 0

        score = ratio * 0.6 + overlap * 0.4
        if score > best_score:
            best_score = score
            best_idx = i

    if best_score >= 0.55:
        return best_idx
    return None

# ── Main ──

# Load datasets
with open(DATASETS_PATH, "r", encoding="utf-8") as f:
    datasets = json.load(f)

# Walk through report directories
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
        datasets[idx]["agent_review"] = {
            "paper_id": info.get("paper_id", ""),
            "scores": info.get("scores", {}),
        }
        matched += 1
        print(f"  MATCHED: {report_name[:60]} → [{datasets[idx]['category']}] {datasets[idx]['name'][:60]}")
    else:
        unmatched.append(report_name)
        print(f"  UNMATCHED: {report_name[:80]}")

# Write back
with open(DATASETS_PATH, "w", encoding="utf-8") as f:
    json.dump(datasets, f, ensure_ascii=False, indent=1)

print(f"\nMatched: {matched}/{len(report_dirs)}")
print(f"Unmatched: {len(unmatched)}")
for u in unmatched:
    print(f"  - {u[:100]}")