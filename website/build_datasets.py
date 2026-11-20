"""Merge raw JSON benchmark sheets into unified English-only datasets.json.

Data source: Kingsoft Docs (https://www.kdocs.cn/l/cbXjea3GKDH7)
snapshotted in summary/raw/*.json
"""
import json, os, re

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "summary", "raw")
OUT_FILE = os.path.join(os.path.dirname(__file__), "AI4M", "datasets.json")

SCHEMA_A_FILES = ["AI\u6a21\u578b\u8bc4\u6d4b.json", "\u751f\u6210\u4e0e\u9006\u5411\u8bbe\u8ba1.json",
                  "\u4f18\u5316\u4e0e\u5b9e\u9a8c\u63a8\u8350.json",
                  "\u8def\u7ebf\u4e0e\u6b65\u9aa4\u89c4\u5212.json", "\u9884\u6d4b\u4e0e\u8bc6\u522b.json"]
SCHEMA_B_FILES = ["\u9006\u5411\u8bbe\u8ba1.json", "\u6027\u8d28\u9884\u6d4b_\u6b63\u5411.json",
                  "\u8fed\u4ee3\u4f18\u5316_\u65f6\u5e8f.json"]

datasets = []
seen = set()

# ═══════════════════════
#  UTILITY
# ═══════════════════════

def clean(v):
    if v is None: return ""
    return str(v).strip()

def is_empty_row(row, fields):
    return not any(clean(row[i]) for i in range(min(len(row), len(fields))))

def is_header_row(row, header):
    matches = 0
    for i in range(min(len(row), len(header))):
        if clean(row[i]) and clean(row[i]) == clean(header[i]):
            matches += 1
    return matches >= 2

def extract_year(s):
    if not s: return ""
    m = re.search(r'(19|20)\d{2}', str(s))
    return m.group(0) if m else str(s).strip()[:20]

def extract_doi(s):
    return str(s).strip() if s else ""

def dedup_key(name, url, cat):
    return f"{clean(name)[:80]}|{clean(url)[:200]}|{cat}"

def has_chinese(s):
    return bool(s) and any('\u4e00' <= c <= '\u9fff' for c in s)

# ═══════════════════════
#  CATEGORY CONSOLIDATION
# ═══════════════════════

CATEGORY_MAP = {
    "AI\u6a21\u578b\u8bc4\u6d4b":      "Benchmarks & Evaluation",
    "\u751f\u6210\u4e0e\u9006\u5411\u8bbe\u8ba1":  "Generation & Inverse Design",
    "\u9006\u5411\u8bbe\u8ba1":        "Generation & Inverse Design",
    "\u6027\u8d28\u9884\u6d4b\uff08\u6b63\u5411\uff09": "Property Prediction",
    "\u9884\u6d4b\u4e0e\u8bc6\u522b":       "Property Prediction",
    "\u8fed\u4ee3\u4f18\u5316\uff08\u65f6\u5e8f\uff09": "Sequential Optimization",
    "\u4f18\u5316\u4e0e\u5b9e\u9a8c\u63a8\u8350":  "Sequential Optimization",
    "\u8def\u7ebf\u4e0e\u6b65\u9aa4\u89c4\u5212":  "Workflow & Data",
}

# ═══════════════════════
#  DATA TYPE NORMALIZATION
# ═══════════════════════

def normalize_data_type(raw):
    s = clean(raw)
    if not s: return ""
    if s.startswith("S ") or "\u6a21\u62df" in s: return "Simulated"
    if s.startswith("E ") or "\u771f\u5b9e" in s: return "Experimental"
    if s.startswith("H ") or "\u6df7\u5408" in s: return "Hybrid"
    return ""

# ═══════════════════════
#  TASK TYPE NORMALIZATION
# ═══════════════════════

def normalize_task_type(raw):
    s = clean(raw)
    if not s: return "Other"
    if "\u751f\u6210" in s or "\u9006\u5411\u8bbe\u8ba1" in s: return "Generation & Inverse Design"
    if "\u9884\u6d4b" in s or "\u8bc6\u522b" in s: return "Prediction"
    if "\u4f18\u5316" in s or "\u5b9e\u9a8c\u63a8\u8350" in s: return "Sequential Optimization"
    if "\u8def\u7ebf" in s or "\u6b65\u9aa4\u89c4\u5212" in s: return "Workflow & Data"
    if "GEN" in s and "PRED" in s: return "Generation & Inverse Design"
    if "GEN" in s: return "Generation & Inverse Design"
    if "PRED" in s: return "Prediction"
    if "SEQ" in s: return "Sequential Optimization"
    if "REAS" in s: return "Workflow & Data"
    if "Data" in s or "data" in s: return "Workflow & Data"
    if "Offline" in s or "MBO" in s: return "Sequential Optimization"
    return "Other"

# ═══════════════════════
#  CHINESE→ENGLISH DICTIONARY (materials science + general)
# ═══════════════════════

_TRANS = {
    # === Materials systems ===
    "\u65e0\u673a": "inorganic", "\u6709\u673a": "organic",
    "\u5206\u5b50": "molecular", "\u6750\u6599": "material",
    "\u6676\u4f53": "crystal", "\u975e\u6676": "amorphous",
    "\u591a\u5b54": "porous", "\u5c42\u72b6": "layered",
    "\u4e8c\u7ef4": "2D", "\u4e09\u7ef4": "3D",
    "\u4e09\u5143": "ternary", "\u4e8c\u5143": "binary",
    "\u56db\u5143": "quaternary", "\u516d\u5143": "hexanary",
    "\u6709\u5e8f": "ordered", "\u65e0\u5e8f": "disordered",
    "\u6676\u4f53\u7ed3\u6784": "crystal structure",
    "\u539f\u5b50\u7ed3\u6784": "atomic structure",
    "\u5206\u5b50\u7ed3\u6784": "molecular structure",
    "\u5316\u5b66\u7ec4\u6210": "chemical composition",
    "\u5316\u5b66\u5f0f\u7ec4\u6210": "chemical formula",
    "\u805a\u5408\u7269": "polymer", "\u5408\u91d1": "alloy",
    "\u91d1\u5c5e": "metal", "\u6c27\u5316\u7269": "oxide",
    "\u9499\u949b\u77ff": "perovskite",
    "\u56fa\u6001\u7535\u89e3\u8d28": "solid electrolyte",
    "\u534a\u5bfc\u4f53": "semiconductor",
    "\u7535\u50ac\u5316": "electrocatalytic", "\u50ac\u5316": "catalytic",
    "\u7eb3\u7c73\u9897\u7c92": "nanoparticle", "\u8584\u819c": "thin film",
    "\u91d1\u5c5e\u6709\u673a\u6846\u67b6": "MOF",
    "\u5171\u4ef7\u6709\u673a\u6846\u67b6": "COF",
    "\u914d\u4f4d\u805a\u5408\u7269": "coordination polymer",
    "MXene": "MXene", "MAX\u76f8": "MAX phase",
    "Heusler": "Heusler", "\u8d85\u6750\u6599": "metamaterial",
    "\u590d\u5408\u6750\u6599": "composite",
    "3D\u6253\u5370": "3D-printed",
    "\u5efa\u7b51\u80f6\u51dd": "cementitious",
    # === Elements ===
    "\u9490": "Pd", "\u9491": "Ir", "\u94c2": "Pt", "\u954d": "Ni",
    "\u94c1": "Fe", "\u94b4": "Co", "\u94dc": "Cu", "\u9530": "Mn",
    "\u94f6": "Ag", "\u91d1": "Au", "\u949b": "Ti", "\u94bd": "Ta",
    "\u54c8": "Hf", "\u9506": "Zr", "\u948c": "Ru", "\u9502": "Li",
    "\u9491": "Na", "\u7845": "Si", "\u78b3": "C", "\u786b": "S",
    "\u6c2e": "N", "\u78f7": "P", "\u6c27": "O",
    "\u786b\u78f7": "thiophosphate",
    "\u7a00\u571f": "rare-earth",
    "\u6c2e\u5316\u7269": "nitride", "\u78b3\u5316\u7269": "carbide",
    "\u786b\u5316\u7269": "sulfide",
    "\u9ad8\u71b5": "high-entropy",
    # === General science ===
    "\u8868\u9762": "surface", "\u754c\u9762": "interface", "\u8fb9\u754c": "boundary",
    "\u6c89\u79ef": "deposition", "\u9009\u62e9\u6027": "selective",
    "\u5206\u79bb": "separation", "\u5076\u8054": "coupling",
    "\u53cd\u5e94": "reaction", "\u82b3\u57fa": "aryl",
    "\u5364\u5316\u7269": "halide", "\u80fa": "amine",
    "\u529b\u5b66": "mechanical", "\u70ed\u529b\u5b66": "thermodynamic",
    "\u58f0\u5b50": "phonon", "\u52a8\u529b\u5b66": "dynamics",
    "\u7535\u5b50\u7ed3\u6784": "electronic structure",
    "\u78c1\u6027": "magnetic", "\u5149\u5b66": "optical",
    "\u8d85\u5bfc": "superconducting",
    "\u5149\u4f0f": "photovoltaic", "\u53d1\u5149": "luminescent",
    "\u751f\u7269\u6d3b\u6027": "bioactivity", "\u86cb\u767d": "protein",
    "\u5316\u5408\u7269": "compound", "\u5143\u7d20": "element",
    "\u5e26\u9699": "band gap", "\u7535\u5b50": "electronic",
    "\u5316\u5b66": "chemical",
    "\u5de5\u827a\u53c2\u6570": "process parameter",
    "\u5b9e\u9a8c\u53c2\u6570": "experimental parameter",
    "\u6c60\u8c6b": "relaxation", "\u8f68\u8ff9": "trajectory",
    "\u6e29\u5ea6": "temperature",
    "\u538b\u529b\u5bb9\u5668": "pressure vessel",
    "\u7ea4\u7ef4": "fiber",
    "\u7ea4\u7ef4\u590d\u5408\u6750\u6599": "fiber composite",
    # === Data / ML / methods ===
    "\u8f93\u5165": "Input", "\u8f93\u51fa": "Output",
    "\u6a21\u6001": "modality", "\u591a\u6a21\u6001": "multimodal",
    "\u5355\u6a21\u6001": "single-modal",
    "\u6570\u503c": "numerical", "\u6a21\u62df": "simulated",
    "\u4eff\u771f": "simulation", "\u6570\u636e\u5e93": "database",
    "\u57fa\u51c6": "benchmark", "\u6a21\u578b": "model",
    "\u8bc4\u4f30": "evaluation", "\u6027\u8d28": "property",
    "\u7ed3\u6784": "structure",
    "\u6570\u636e\u96c6": "dataset", "\u6570\u636e": "data",
    "\u7b97\u6cd5": "algorithm", "\u8bad\u7ec3": "training",
    "\u9884\u8bad\u7ec3": "pretrained",
    "\u8bad\u7ec3\u96c6": "training set", "\u6d4b\u8bd5\u96c6": "test set",
    "\u9a8c\u8bc1": "validation", "\u6d4b\u8bd5": "test",
    "\u57fa\u7ebf": "baseline", "\u5bf9\u6bd4": "comparison",
    "\u6bd4\u8f83": "comparing",
    "\u4efb\u52a1": "task", "\u8ba1\u7b97": "computational",
    "\u7f51\u683c": "grid", "\u968f\u673a": "random",
    "\u968f\u673a\u91c7\u6837": "random sampling",
    "\u6761\u4ef6": "conditional", "\u6821\u51c6": "calibration",
    # === Quantities / phrases ===
    "\u6bcf\u4e2a": "each", "\u5019\u9009": "candidate",
    "\u5b9e\u9a8c\u7ec4": "experimental group",
    "\u53d1\u73b0\u6848\u4f8b": "discovery case",
    "\u53d1\u73b0": "discovery",
    "\u6846\u67b6": "framework",
    "\u8d85\u8fc7": "over", "\u63d0\u4f9b": "provides",
    "\u516c\u5f00": "public", "\u521d\u59cb": "initial",
    "\u7528\u4e8e": "for", "\u6db5\u76d6": "covers",
    "\u5b50\u96c6": "subset", "\u539f\u59cb": "original",
    "\u91cd\u590d": "repeat", "\u9884\u7b97": "budget",
    "\u7a33\u5b9a": "stable", "\u5339\u914d": "matching",
    "\u4ee5\u53ca": "and", "\u5305\u542b": "containing",
    "\u4e3b\u8981\u5305\u62ec": "mainly including",
    "\u4e3b\u8981\u662f": "primarily",
    "\u4e5f\u5305\u542b": "also including",
    "\u4f53\u7cfb": "system", "\u94fe\u63a5": "link",
    # === Numbers ===
    "\u4e07\u6761": "10k entries", "\u4e07\u4e2a": "10k items",
    "\u4e2a\u968f\u673a\u79cd\u5b50": "random seeds",
    "\u79cd\u65b9\u6cd5": "methods",
    "\u6570\u636e\u70b9": "data points",
    "\u5206\u5b50\u5f0f": "molecular formula",
    # === Other common ===
    "\u8fde\u7eed": "continuous", "\u79bb\u6563": "discrete",
    "\u5e8f\u5217": "sequence", "\u65f6\u5e8f": "temporal",
    "\u751f\u6210": "generation", "\u7b5b\u9009": "screening",
    "\u641c\u7d22": "search", "\u8bbe\u8ba1": "design",
    "\u5408\u6210": "synthesis", "\u8868\u5f81": "characterization",
    "\u8c31\u56fe": "spectrum", "\u5f00\u6e90": "open-source",
    "\u7248\u672c": "version", "\u66f4\u65b0": "updated",
    "\u56fa\u5b9a": "fixed", "\u8bc4\u6d4b": "evaluation",
    "\u6709\u6548\u6027": "validity", "\u552f\u4e00\u6027": "uniqueness",
    "\u65b0\u9896\u6027": "novelty", "\u7a33\u5b9a\u6027": "stability",
    "\u53d1\u73b0\u4ef7\u503c": "discovery value",
    "\u5206\u5e03\u8986\u76d6": "distribution coverage",
    "\u5206\u5e03\u8ddd\u79bb": "distribution distance",
    "\u6240\u6709": "all", "\u90e8\u5206": "partial",
    "\u4e3b": "main", "\u57fa\u4e8e": "based on",
    "\u7ed3\u5408": "combining", "\u91c7\u7528": "using",
    "\u8fdb\u884c": "performed", "\u901a\u8fc7": "via",
    "\u91cd\u7b97": "recomputing", "\u63d0\u793a": "prompt",
    "\u7cbe\u5ea6": "precision", "\u56de\u53ec": "recall",
    "\u6d41\u6c34\u7ebf": "pipeline", "\u7279\u5f81": "feature",
    "\u5143\u6570\u636e": "metadata",
    "\u53c2\u8003\u6587\u732e": "reference", "\u77e5\u8bc6\u56fe\u8c31": "knowledge graph",
    "\u6ce8\u610f": "note", "\u5b58\u50a8": "storage",
    "\u683c\u5f0f": "format",
    # === Crystallography / specific ===
    "CIF": "CIF", "VASP": "VASP", "DFT": "DFT",
    "DOE": "DOE",
    "AD": "AD",
    "\u51f8\u5305": "convex hull",
    "\u5f62\u6210\u80fd": "formation energy",
    "SPG": "space group",
    "ICSD": "ICSD",
    "\u8d28\u5b50\u4f20\u5bfc\u7387": "proton conductivity",
    "\u5e7f\u4e49\u68af\u5ea6\u8fd1\u4f3c": "GGA",
}

def translate_cn(text):
    """Translate Chinese text to English using dictionary replacement.
    If untranslated Chinese remains, strip CJK characters."""
    if not text:
        return ""

    # Always normalize fullwidth punctuation
    s = text
    s = s.replace('\uff08', '(').replace('\uff09', ')')   # （）
    s = s.replace('\uff0c', ', ').replace('\uff1b', '; ')
    s = s.replace('\uff1a', ': ').replace('\u3001', '/')
    s = s.replace('‘', "'").replace('’', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', '--').replace('–', '-')

    if not has_chinese(s):
        return s

    # Sort by length descending to replace longer phrases first
    for cn, en in sorted(_TRANS.items(), key=lambda x: -len(x[0])):
        s = s.replace(cn, f" {en} ")

    # If Chinese still remains, strip CJK chars
    if has_chinese(s):
        s = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+', ' ', s)

    # Normalize whitespace and clean up
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*,\s*', ', ', s)
    s = re.sub(r'\s*;\s*', '; ', s)
    s = re.sub(r'\s*:\s*', ': ', s)
    s = re.sub(r'\s*/\s*', '/', s)
    s = re.sub(r'^[,;:./\s]+', '', s)
    s = re.sub(r'[,;:./\s]+$', '', s)
    s = re.sub(r'\s+', ' ', s).strip()

    if not s:
        return ""
    # Capitalize first letter
    s = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
    return s

def build_description(name, cat_en, task_en, mat_en, scale_en, dtype_en, usage_en, extra=None):
    """Construct a clean English description from structured fields."""
    parts = []
    if task_en and task_en != "Other":
        parts.append(f"Benchmark for {task_en.lower()} tasks")
    if mat_en:
        parts.append(f"in {mat_en}")

    if parts:
        result = " ".join(parts) + "."
    else:
        result = ""

    info = []
    if dtype_en and dtype_en != "Other":
        info.append(f"{dtype_en} data")
    if scale_en:
        info.append(scale_en)
    if info:
        result += " Contains " + "; ".join(info) + "."

    if usage_en:
        result += f" Usage: {usage_en}"

    # Include structured extra info if available (from Schema B)
    if extra:
        result += " " + extra

    return result[:600] if result else "(no description)"

# ═══════════════════════
#  PROCESS SCHEMA A
# ═══════════════════════

for fname in SCHEMA_A_FILES:
    fpath = os.path.join(RAW_DIR, fname)
    if not os.path.exists(fpath):
        print(f"SKIP (not found): {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    sheet_name = data["name"]
    header = data["header"]
    rows = data["rows"]

    def find_col(keywords):
        for i, h in enumerate(header):
            hl = clean(h)
            for kw in keywords:
                if kw in hl:
                    return i
        return -1

    idx_name = find_col(["\u6570\u636e\u96c6\u540d\u79f0", "\u540d\u79f0"])
    idx_url = find_col(["\u6570\u636e\u96c6\u5730\u5740", "\u5730\u5740", "URL", "url"])
    idx_year = find_col(["\u53d1\u5e03\u5e74\u4efd", "\u5e74\u4efd", "Year"])
    idx_desc = find_col(["\u6570\u636e\u5185\u5bb9", "\u5185\u5bb9", "\u63cf\u8ff0"])
    idx_scale = find_col(["\u6570\u636e\u89c4\u6a21", "\u89c4\u6a21", "\u4f53\u91cf"])
    idx_dtype = find_col(["\u6570\u636e\u7c7b\u578b"])
    idx_task = find_col(["\u4efb\u52a1\u7c7b\u578b"])
    idx_usage = find_col(["\u672c\u9636\u6bb5\u5177\u4f53\u7528\u9014", "\u5177\u4f53\u7528\u9014", "\u7528\u9014"])
    idx_doi = find_col(["\u539f\u59cb\u53d1\u5e03\u6587\u732e", "DOI", "doi"])
    idx_bib = find_col(["\u5f15\u6587\u683c\u5f0f", "bib"])
    idx_material = find_col(["\u6750\u6599\u4f53\u7cfb"])
    idx_baseline = find_col(["\u57fa\u7ebf\u6a21\u578b", "baseline", "Baseline"])

    for row in rows:
        if is_empty_row(row, header) or is_header_row(row, header):
            continue
        name = translate_cn(clean(row[idx_name]) if idx_name >= 0 and idx_name < len(row) else "")
        url = clean(row[idx_url]) if idx_url >= 0 and idx_url < len(row) else ""
        if not name and not url:
            continue
        year = extract_year(clean(row[idx_year])) if idx_year >= 0 and idx_year < len(row) else ""
        cn_desc = clean(row[idx_desc]) if idx_desc >= 0 and idx_desc < len(row) else ""
        scale = clean(row[idx_scale]) if idx_scale >= 0 and idx_scale < len(row) else ""
        dtype = clean(row[idx_dtype]) if idx_dtype >= 0 and idx_dtype < len(row) else ""
        task = clean(row[idx_task]) if idx_task >= 0 and idx_task < len(row) else ""
        usage = clean(row[idx_usage]) if idx_usage >= 0 and idx_usage < len(row) else ""
        doi = clean(row[idx_doi]) if idx_doi >= 0 and idx_doi < len(row) else ""
        bib = clean(row[idx_bib]) if idx_bib >= 0 and idx_bib < len(row) else ""
        material = clean(row[idx_material]) if idx_material >= 0 and idx_material < len(row) else ""
        baseline = clean(row[idx_baseline]) if idx_baseline >= 0 and idx_baseline < len(row) else ""

        key = dedup_key(name, url, sheet_name)
        if key in seen: continue
        seen.add(key)

        cat_en = CATEGORY_MAP.get(sheet_name, sheet_name)
        task_en = normalize_task_type(task if task else sheet_name)
        dt_en = normalize_data_type(dtype)
        mat_en = translate_cn(material)
        sc_en = translate_cn(scale)
        use_en = translate_cn(usage)
        bl_en = translate_cn(baseline)
        bib_en = translate_cn(bib)
        desc_en = build_description(name, cat_en, task_en, mat_en, sc_en, dt_en, use_en)

        datasets.append({
            "name": name, "url": url, "year": year,
            "category": cat_en, "description": desc_en,
            "scale": sc_en, "data_type": dt_en,
            "task_type": task_en, "usage": use_en,
            "doi": doi, "bib": bib_en,
            "material_system": mat_en, "baseline": bl_en,
            "score": 0, "source_sheet": sheet_name,
        })

# ═══════════════════════
#  PROCESS SCHEMA B
# ═══════════════════════

for fname in SCHEMA_B_FILES:
    fpath = os.path.join(RAW_DIR, fname)
    if not os.path.exists(fpath):
        print(f"SKIP (not found): {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    sheet_name = data["name"]
    header = data["header"]
    rows = data["rows"]

    def find_col_b(keywords):
        for i, h in enumerate(header):
            hl = clean(h)
            for kw in keywords:
                if kw in hl:
                    return i
        return -1

    idx_pid = find_col_b(["Paper ID", "DOI", "paper_id"])
    idx_title = find_col_b(["\u6587\u732e\u540d\u79f0", "\u540d\u79f0", "title"])
    idx_task_code = find_col_b(["\u4efb\u52a1\u4ee3\u7801", "\u4efb\u52a1"])
    idx_material = find_col_b(["\u6750\u6599\u4f53\u7cfb"])
    idx_io = find_col_b(["\u8f93\u5165/\u8f93\u51fa", "\u8f93\u5165"])
    idx_modality = find_col_b(["\u6a21\u6001\u7c7b\u578b", "\u6a21\u6001"])
    idx_source = find_col_b(["\u6570\u636e\u6765\u6e90", "snapshot", "\u6765\u6e90"])
    idx_scale = find_col_b(["\u4f53\u91cf", "\u89c4\u6a21"])
    idx_metrics = find_col_b(["\u6307\u6807"])
    idx_baseline = find_col_b(["Baseline", "baseline"])
    idx_pros = find_col_b(["\u4f18\u70b9"])
    idx_note = find_col_b(["\u5907\u6ce8"])

    for row in rows:
        if is_empty_row(row, header) or is_header_row(row, header):
            continue
        pid = clean(row[idx_pid]) if idx_pid >= 0 and idx_pid < len(row) else ""
        title = clean(row[idx_title]) if idx_title >= 0 and idx_title < len(row) else ""
        if not pid and not title:
            continue

        task_code = clean(row[idx_task_code]) if idx_task_code >= 0 and idx_task_code < len(row) else ""
        material = clean(row[idx_material]) if idx_material >= 0 and idx_material < len(row) else ""
        io_desc = clean(row[idx_io]) if idx_io >= 0 and idx_io < len(row) else ""
        modality = clean(row[idx_modality]) if idx_modality >= 0 and idx_modality < len(row) else ""
        source = clean(row[idx_source]) if idx_source >= 0 and idx_source < len(row) else ""
        scale = clean(row[idx_scale]) if idx_scale >= 0 and idx_scale < len(row) else ""
        metrics = clean(row[idx_metrics]) if idx_metrics >= 0 and idx_metrics < len(row) else ""
        baseline = clean(row[idx_baseline]) if idx_baseline >= 0 and idx_baseline < len(row) else ""
        pros = clean(row[idx_pros]) if idx_pros >= 0 and idx_pros < len(row) else ""
        note = clean(row[idx_note]) if idx_note >= 0 and idx_note < len(row) else ""

        name = translate_cn(title if title else pid)
        url = pid if pid.startswith("http") else (f"https://doi.org/{pid}" if pid.startswith("10.") else pid)
        doi = pid if pid.startswith("10.") else ""
        year = ""

        cat_en = CATEGORY_MAP.get(sheet_name, sheet_name)
        task_en = normalize_task_type(task_code if task_code else sheet_name)
        dt_en = normalize_data_type(modality)
        mat_en = translate_cn(material)
        sc_en = translate_cn(scale)
        bl_en = translate_cn(baseline)
        note_en = translate_cn(note)

        # Build extra info from Schema B fields (in English)
        extra_parts = []
        if io_desc:
            extra_parts.append(f"I/O: {translate_cn(io_desc)}")
        if source:
            extra_parts.append(f"Source: {translate_cn(source)}")
        if metrics:
            extra_parts.append(f"Metrics: {translate_cn(metrics)}")
        if pros:
            extra_parts.append(f"Strengths: {translate_cn(pros)}")
        extra = " | ".join(extra_parts)

        desc_en = build_description(name, cat_en, task_en, mat_en, sc_en, dt_en, note_en, extra)

        key = dedup_key(name, url, sheet_name)
        if key in seen: continue
        seen.add(key)

        datasets.append({
            "name": name, "url": url, "year": year,
            "category": cat_en, "description": desc_en,
            "scale": sc_en, "data_type": dt_en,
            "task_type": task_en, "usage": note_en,
            "doi": doi, "bib": "",
            "material_system": mat_en, "baseline": bl_en,
            "score": 0, "source_sheet": sheet_name,
        })

# ═══════════════════════
#  LOAD SCORES
# ═══════════════════════

reg_path = os.path.join(os.path.dirname(__file__), "..", "summary", "scored_registry.json")
if os.path.exists(reg_path):
    with open(reg_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    for entry in registry.get("entries", {}).values():
        pid = clean(entry.get("paper_id", ""))
        x5 = entry.get("x5_final", 0)
        level = entry.get("level", 0)
        if pid and x5:
            for ds in datasets:
                ds_url = clean(ds.get("url", ""))
                ds_doi = clean(ds.get("doi", ""))
                if pid.lower() in ds_url.lower() or pid.lower() in ds_doi.lower():
                    ds["score"] = round(x5, 2)
                    ds["level"] = level
                    ds["level_label"] = entry.get("level_label", "")

# ═══════════════════════
#  WRITE OUTPUT
# ═══════════════════════

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(datasets, f, ensure_ascii=False, indent=1)

print(f"Done! {len(datasets)} datasets written to {OUT_FILE}")

# Stats
cats = {}
for ds in datasets:
    c = ds["category"]
    cats[c] = cats.get(c, 0) + 1
print("\n--- Category stats ---")
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}")

# Check for remaining Chinese
cn = 0
for ds in datasets:
    for field in ['category','description','scale','data_type','task_type','usage','material_system','baseline']:
        if has_chinese(ds.get(field,'')):
            cn += 1
            break
print(f"\nDatasets with remaining Chinese: {cn}/{len(datasets)}")