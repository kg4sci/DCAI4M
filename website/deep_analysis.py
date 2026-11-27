"""Deep analysis of AI4M dataset distribution and scoring patterns."""
import json, os, statistics
from collections import defaultdict

DATA_PATH = os.path.join(os.path.dirname(__file__), "AI4M", "datasets.json")
d = json.load(open(DATA_PATH, encoding="utf-8"))

X_DIMS = ["O","A","I","G","U","P"]
Y_DIMS = ["E","R","C"]
ALL_DIMS = X_DIMS + Y_DIMS
DIM_NAMES = {
    "O":"Output & Decision","A":"Adaptivity & Sequentiality","I":"Workflow Integration",
    "G":"Goal & Constraint","U":"Uncertainty & Failure","P":"Autonomy & Actionability",
    "E":"Exp. Dependence","R":"Exp. Alignment","C":"Exp. Completeness"
}

def get_scores(entry, review_type="agent_review"):
    r = entry.get(review_type, {})
    return r.get("scores", {})

def avg(vals):
    vals = [v for v in vals if isinstance(v,(int,float))]
    return sum(vals)/len(vals) if vals else 0

def pct(n, total):
    return f"{n}/{total} ({n/total*100:.0f}%)" if total else "0"

# ═══════════════════════════════════════
# 1. Overall landscape
# ═══════════════════════════════════════
print("=" * 70)
print("AI4M DATA DISTRIBUTION & SCORING DEEP ANALYSIS")
print("=" * 70)

total = len(d)
scored = [x for x in d if x.get("score",0) > 0]
has_agent = [x for x in d if x.get("agent_review")]
has_expert = [x for x in d if x.get("expert_review")]
print(f"\nTotal datasets: {total}")
print(f"With composite score: {len(scored)} ({len(scored)/total*100:.0f}%)")
print(f"With agent review: {len(has_agent)}")
print(f"With expert review: {len(has_expert)}")

# ═══════════════════════════════════════
# 2. Category × Task Type cross-tab
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("2. CATEGORY × TASK TYPE DISTRIBUTION")
print("=" * 70)

cats = sorted(set(x.get("category","?") for x in d))
tasks = sorted(set(x.get("task_type","?") for x in d if x.get("task_type")))

matrix = defaultdict(lambda: defaultdict(int))
for x in d:
    c = x.get("category","?")
    t = x.get("task_type","?")
    matrix[c][t] += 1

print(f"\n{'Category':<30}", end="")
for t in tasks: print(f"{t[:18]:>18}", end="")
print(f"{'Total':>8}")
print("-" * (30 + 18*len(tasks) + 8))
for c in cats:
    print(f"{c:<30}", end="")
    row_total = 0
    for t in tasks:
        v = matrix[c][t]
        row_total += v
        print(f"{v:>18}", end="")
    print(f"{row_total:>8}")

# ═══════════════════════════════════════
# 3. Data Type distribution
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("3. DATA TYPE DISTRIBUTION BY CATEGORY")
print("=" * 70)

dtypes = ["Simulated","Experimental","Hybrid","(unspecified)"]
dt_matrix = defaultdict(lambda: defaultdict(int))
for x in d:
    c = x.get("category","?")
    dt = x.get("data_type","") or "(unspecified)"
    dt_matrix[c][dt] += 1

print(f"\n{'Category':<30}", end="")
for dt in dtypes: print(f"{dt:>14}", end="")
print()
print("-" * (30 + 14*len(dtypes)))
for c in cats:
    print(f"{c:<30}", end="")
    for dt in dtypes:
        print(f"{dt_matrix[c][dt]:>14}", end="")
    print()

# Data type coverage
dt_counts = defaultdict(int)
for x in d:
    dt_counts[x.get("data_type","") or "(unspecified)"] += 1
print(f"\nOverall: {dict(dt_counts)}")
print(f"Data type coverage: {sum(1 for x in d if x.get('data_type'))}/{total} ({sum(1 for x in d if x.get('data_type'))/total*100:.0f}%)")

# ═══════════════════════════════════════
# 4. Work stage analysis (from source_sheet)
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("4. WORK STAGE DISTRIBUTION (source sheet → research phase)")
print("=" * 70)

stage_map = {
    "AI模型评测": "Benchmarking & Evaluation",
    "生成与逆向设计": "Generation & Design",
    "逆向设计": "Generation & Design",
    "性质预测（正向）": "Property Prediction",
    "预测与识别": "Property Prediction",
    "迭代优化（时序）": "Sequential Optimization",
    "优化与实验推荐": "Sequential Optimization",
    "路线与步骤规划": "Workflow & Planning",
}
stage_counts = defaultdict(int)
stage_scored = defaultdict(list)
for x in d:
    ss = x.get("source_sheet","?").strip()
    stage = stage_map.get(ss, ss)
    stage_counts[stage] += 1
    if x.get("score",0) > 0:
        stage_scored[stage].append(x["score"])

print(f"\n{'Work Stage':<30}{'Count':>8}{'Scored':>8}{'Avg Score':>12}")
print("-" * 58)
for stage in sorted(stage_counts.keys()):
    n = stage_counts[stage]
    ns = len(stage_scored[stage])
    avg_s = avg(stage_scored[stage])
    print(f"{stage:<30}{n:>8}{ns:>8}{avg_s:>12.2f}")

# ═══════════════════════════════════════
# 5. X-axis scoring deep dive
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("5. X-AXIS (TASK INTELLIGENCE) SCORING ANALYSIS")
print("=" * 70)

# 5a. Overall dimension stats
print("\n5a. Dimension-level statistics (agent scores, n=91)")
print(f"\n{'Dim':<4}{'Name':<30}{'Mean':>8}{'Std':>8}{'Min':>6}{'Max':>6}{'Mode':>6}")
print("-" * 68)
for dim in X_DIMS:
    vals = [get_scores(x).get(dim) for x in has_agent]
    nums = [v for v in vals if isinstance(v,(int,float))]
    if nums:
        mean_v = statistics.mean(nums)
        std_v = statistics.stdev(nums) if len(nums)>1 else 0
        mode_v = statistics.mode(nums)
        print(f"{dim:<4}{DIM_NAMES[dim]:<30}{mean_v:>8.2f}{std_v:>8.2f}{min(nums):>6}{max(nums):>6}{mode_v:>6}")

# 5b. By category
print("\n5b. X-axis mean scores by category (agent)")
print(f"\n{'Category':<30}", end="")
for dim in X_DIMS: print(f"{dim:>6}", end="")
print(f"{'X-avg':>8}")
print("-" * (30 + 6*len(X_DIMS) + 8))
for c in cats:
    entries = [x for x in has_agent if x.get("category")==c]
    if not entries: continue
    print(f"{c:<30}", end="")
    dim_avgs = []
    for dim in X_DIMS:
        vals = [get_scores(x).get(dim) for x in entries]
        nums = [v for v in vals if isinstance(v,(int,float))]
        a = avg(nums)
        dim_avgs.append(a)
        print(f"{a:>6.2f}", end="")
    print(f"{avg(dim_avgs):>8.2f}")

# 5c. Score distribution per dimension
print("\n5c. Score distribution per X dimension (agent)")
for dim in X_DIMS:
    vals = [get_scores(x).get(dim) for x in has_agent]
    nums = [v for v in vals if isinstance(v,(int,float))]
    dist = defaultdict(int)
    for v in nums: dist[int(v)] += 1
    bar = " ".join(f"{k}:{dist.get(k,0)}" for k in range(5))
    print(f"  {dim} ({DIM_NAMES[dim]}): {bar}")

# ═══════════════════════════════════════
# 6. Y-axis scoring deep dive
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("6. Y-AXIS (EXPERIMENTAL ORIENTATION) SCORING ANALYSIS")
print("=" * 70)

print("\n6a. Dimension-level statistics (agent scores)")
print(f"\n{'Dim':<4}{'Name':<35}{'Mean':>8}{'0':>6}{'1':>6}{'2':>6}")
print("-" * 65)
for dim in Y_DIMS:
    vals = [get_scores(x).get(dim) for x in has_agent]
    nums = [v for v in vals if isinstance(v,(int,float))]
    dist = defaultdict(int)
    for v in nums: dist[int(v)] += 1
    mean_v = avg(nums)
    print(f"{dim:<4}{DIM_NAMES[dim]:<35}{mean_v:>8.2f}{dist.get(0,0):>6}{dist.get(1,0):>6}{dist.get(2,0):>6}")

print("\n6b. Y-axis mean scores by category (agent)")
print(f"\n{'Category':<30}", end="")
for dim in Y_DIMS: print(f"{dim:>6}", end="")
print(f"{'Y-avg':>8}")
print("-" * (30 + 6*len(Y_DIMS) + 8))
for c in cats:
    entries = [x for x in has_agent if x.get("category")==c]
    if not entries: continue
    print(f"{c:<30}", end="")
    dim_avgs = []
    for dim in Y_DIMS:
        vals = [get_scores(x).get(dim) for x in entries]
        nums = [v for v in vals if isinstance(v,(int,float))]
        a = avg(nums)
        dim_avgs.append(a)
        print(f"{a:>6.2f}", end="")
    print(f"{avg(dim_avgs):>8.2f}")

# ═══════════════════════════════════════
# 7. Agent vs Expert comparison
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("7. AGENT vs EXPERT SCORE COMPARISON")
print("=" * 70)

both = [x for x in d if x.get("agent_review") and x.get("expert_review")]
print(f"\nDatasets with both reviews: {len(both)}")

print(f"\n{'Dim':<4}{'Agent Mean':>12}{'Expert Mean':>12}{'Gap (A-E)':>12}{'Agreement':>12}")
print("-" * 52)
for dim in ALL_DIMS:
    a_vals = [get_scores(x,"agent_review").get(dim) for x in both]
    e_vals = [get_scores(x,"expert_review").get(dim) for x in both]
    a_nums = [v for v in a_vals if isinstance(v,(int,float))]
    e_nums = [v for v in e_vals if isinstance(v,(int,float))]
    a_mean = avg(a_nums)
    e_mean = avg(e_nums)
    # Agreement: fraction where |a-e| <= 0.5
    pairs = [(a,e) for a,e in zip(a_vals,e_vals) if isinstance(a,(int,float)) and isinstance(e,(int,float))]
    agree = sum(1 for a,e in pairs if abs(a-e)<=0.5)
    agree_pct = agree/len(pairs)*100 if pairs else 0
    print(f"{dim:<4}{a_mean:>12.2f}{e_mean:>12.2f}{a_mean-e_mean:>+12.2f}{agree_pct:>11.0f}%")

# Biggest disagreements
print("\n7b. Largest agent-expert disagreements (top 10)")
disagreements = []
for x in both:
    a_sc = get_scores(x,"agent_review")
    e_sc = get_scores(x,"expert_review")
    for dim in ALL_DIMS:
        av = a_sc.get(dim)
        ev = e_sc.get(dim)
        if isinstance(av,(int,float)) and isinstance(ev,(int,float)):
            gap = abs(av-ev)
            if gap >= 1.5:
                disagreements.append((gap, x["name"][:50], dim, av, ev))
disagreements.sort(reverse=True)
for gap, name, dim, av, ev in disagreements[:10]:
    print(f"  {dim}: Agent={av} Expert={ev} (gap={gap:.1f}) — {name}")

# ═══════════════════════════════════════
# 8. Data Type × Scoring
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("8. DATA TYPE × SCORING PATTERNS")
print("=" * 70)

for dt in ["Simulated","Experimental","Hybrid"]:
    entries = [x for x in has_agent if x.get("data_type")==dt]
    if not entries: continue
    print(f"\n{dt} (n={len(entries)}):")
    # X-axis
    x_avgs = []
    for dim in X_DIMS:
        vals = [get_scores(x).get(dim) for x in entries]
        nums = [v for v in vals if isinstance(v,(int,float))]
        x_avgs.append(avg(nums))
    # Y-axis
    y_avgs = []
    for dim in Y_DIMS:
        vals = [get_scores(x).get(dim) for x in entries]
        nums = [v for v in vals if isinstance(v,(int,float))]
        y_avgs.append(avg(nums))
    comp_scores = [x.get("score",0) for x in entries if x.get("score",0)>0]
    print(f"  X-axis avg: {avg(x_avgs):.2f}  |  Y-axis avg: {avg(y_avgs):.2f}  |  Composite avg: {avg(comp_scores):.2f}")
    print(f"  X dims: {' '.join(f'{d}={v:.1f}' for d,v in zip(X_DIMS,x_avgs))}")
    print(f"  Y dims: {' '.join(f'{d}={v:.1f}' for d,v in zip(Y_DIMS,y_avgs))}")

# ═══════════════════════════════════════
# 9. Temporal trends
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("9. TEMPORAL TRENDS (scored datasets by year)")
print("=" * 70)

year_scores = defaultdict(list)
year_counts = defaultdict(int)
for x in d:
    y = x.get("year","")
    if y and y.isdigit():
        year_counts[y] += 1
        if x.get("score",0) > 0:
            year_scores[y].append(x["score"])

print(f"\n{'Year':<8}{'Total':>8}{'Scored':>8}{'Avg Score':>12}")
print("-" * 36)
for y in sorted(year_counts.keys()):
    if int(y) >= 2018:
        n = year_counts[y]
        ns = len(year_scores[y])
        a = avg(year_scores[y])
        print(f"{y:<8}{n:>8}{ns:>8}{a:>12.2f}")

# ═══════════════════════════════════════
# 10. Key findings
# ═══════════════════════════════════════
print("\n" + "=" * 70)
print("10. KEY FINDINGS & INSIGHTS")
print("=" * 70)

# Find highest/lowest scoring categories
cat_scores = {}
for c in cats:
    entries = [x for x in scored if x.get("category")==c]
    if entries:
        cat_scores[c] = avg([x["score"] for x in entries])

print("\n10a. Category ranking by composite score:")
for c, s in sorted(cat_scores.items(), key=lambda x:-x[1]):
    print(f"  {c}: {s:.2f}")

# X-axis weakest dimensions
print("\n10b. Weakest X-axis dimensions (lowest mean):")
x_means = {}
for dim in X_DIMS:
    vals = [get_scores(x).get(dim) for x in has_agent]
    nums = [v for v in vals if isinstance(v,(int,float))]
    x_means[dim] = avg(nums)
for dim, m in sorted(x_means.items(), key=lambda x:x[1]):
    print(f"  {dim} ({DIM_NAMES[dim]}): {m:.2f}")

# Y-axis coverage
print("\n10c. Experimental orientation coverage:")
for dim in Y_DIMS:
    vals = [get_scores(x).get(dim) for x in has_agent]
    nums = [v for v in vals if isinstance(v,(int,float))]
    zero_pct = sum(1 for v in nums if v==0)/len(nums)*100 if nums else 0
    print(f"  {dim} ({DIM_NAMES[dim]}): {zero_pct:.0f}% scored 0 (no experimental component)")

# Data type gap
print("\n10d. Data type gap:")
print(f"  {sum(1 for x in d if not x.get('data_type'))}/{total} datasets ({sum(1 for x in d if not x.get('data_type'))/total*100:.0f}%) have NO data type specified")
print(f"  Only {sum(1 for x in d if x.get('data_type')=='Experimental')}/{total} ({sum(1 for x in d if x.get('data_type')=='Experimental')/total*100:.0f}%) are purely Experimental")

# Agent-expert systematic bias
print("\n10e. Agent vs Expert systematic bias:")
a_all = []
e_all = []
for x in both:
    for dim in ALL_DIMS:
        av = get_scores(x,"agent_review").get(dim)
        ev = get_scores(x,"expert_review").get(dim)
        if isinstance(av,(int,float)) and isinstance(ev,(int,float)):
            a_all.append(av)
            e_all.append(ev)
print(f"  Agent overall mean: {avg(a_all):.2f}")
print(f"  Expert overall mean: {avg(e_all):.2f}")
print(f"  Systematic gap: {avg(a_all)-avg(e_all):+.2f}")

print("\n" + "=" * 70)
print("END OF ANALYSIS")
print("=" * 70)