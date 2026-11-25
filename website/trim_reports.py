"""Trim evaluation reports to compact versions — keep scores + notes, drop verbose evidence sections."""
import os, re

REVIEWS_DIR = os.path.join(os.path.dirname(__file__), "AI4M", "reviews")

def trim_report(text):
    """Keep: header block, score tables, final notes. Drop: individual evidence sections."""
    lines = text.split('\n')
    out = []
    in_evidence = False  # skip detailed evidence sections
    skip_until_next_section = False

    for line in lines:
        # Detect evidence sections (开始 detailed breakdown per dimension)
        if re.match(r'^## (初评|独立审查|最终裁决|[OAIUGPERC] ·)', line):
            in_evidence = True
            out.append(line)
            out.append('')  # Keep section header but skip body
            continue

        if in_evidence:
            # Stop when we hit a non-evidence section
            if re.match(r'^## (评分修订记录|局限与待复核)', line):
                in_evidence = False
                out.append(line)
                continue
            if re.match(r'^## (?!.*证据)', line) and not re.match(r'^### (证据|分档条件核对|独立审查意见|主 Agent)', line):
                in_evidence = False
                out.append(line)
                continue
            # Skip evidence body lines, but keep score/status lines
            if re.match(r'^(\*\*评分\*\*|\*\*对应标准\*\*|\*\*判定理由\*\*|\*\*分档比较\*\*|\*\*任务归属\*\*|\*\*边界)', line):
                out.append(line)
                continue
            # Skip everything else in evidence section
            continue

        # Before evidence sections: keep everything (header, summary table)
        out.append(line)

    return '\n'.join(out)


def main():
    files = sorted([f for f in os.listdir(REVIEWS_DIR) if f.endswith('.md')])
    before_total = 0
    after_total = 0

    for fname in files:
        fpath = os.path.join(REVIEWS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()
        before_total += len(text)

        trimmed = trim_report(text)
        after_total += len(trimmed)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(trimmed)

        reduction = (1 - len(trimmed)/len(text)) * 100
        print(f"  {fname}: {len(text):,} → {len(trimmed):,} chars ({reduction:.0f}%)")

    print(f"\nTotal: {before_total/1024:.0f} KB → {after_total/1024:.0f} KB ({(1-after_total/before_total)*100:.0f}% reduced)")

if __name__ == '__main__':
    main()