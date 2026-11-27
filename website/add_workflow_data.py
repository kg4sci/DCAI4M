"""Add new Workflow & Data datasets (from online sheet 路线与步骤规划) to website datasets.json.

Each new entry gets English fields and a two-axis agent_review scored from the
online table evidence (evidence_source=table), following the materials-benchmark
rubric caps (static data resources: A<=1, P<=1).
Composite score = mean of the 9 dimension scores (consistent with update_scores.py).
"""
import json, os

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "AI4M", "datasets.json")

# (name, year, data_type, url, doi, material_system, scale, description, usage,
#   X[O,A,I,G,U,P], Y[E,R,C])
NEW = [
 ("Machine-learned codified synthesis parameters of oxide materials", "2017", "Experimental",
  "https://doi.org/10.1038/sdata.2017.127", "10.1038/sdata.2017.127", "Inorganic oxides",
  "640,000+ source papers; 30 oxide systems",
  "Text-mined oxide synthesis parameters (material system, synthesis conditions) forming a synthesis-parameter knowledge base.",
  "Find existing synthesis strategies for a target material; provide synthesis parameter references.",
  [2,0,2,2,0,0],[1,2,1]),
 ("Text-mined dataset of inorganic materials synthesis recipes", "2019", "Experimental",
  "https://doi.org/10.1038/s41597-019-0224-1", "10.1038/s41597-019-0224-1", "Inorganic; solid-state",
  "~19,500 synthesis records from 53,538 solid-state paragraphs",
  "Literature-extracted target materials, precursors, synthesis operations, conditions and balanced reaction equations.",
  "Identify precursors; learn precursor-to-product synthesis routes; predict mixing/heating operations and conditions.",
  [2,0,2,2,0,0],[1,2,1]),
 ("Dataset of solution-based inorganic materials synthesis procedures", "2022", "Experimental",
  "https://doi.org/10.1038/s41597-022-01317-2", "10.1038/s41597-022-01317-2", "Inorganic; hydrothermal/precipitation",
  "35,675 records (20,037 hydrothermal; 15,638 precipitation)",
  "Literature-extracted targets, precursors, amounts, solvents, operations and process conditions with reaction equations.",
  "Precursor/solvent selection; learn hydrothermal/precipitation routes; predict amounts, operations and conditions.",
  [2,0,2,2,0,0],[1,2,2]),
 ("TMSR (Thermoelectric Materials Synthesis Recipes)", "2023", "Experimental",
  "https://doi.org/10.1021/acs.chemmater.3c01834", "10.1021/acs.chemmater.3c01834", "Thermoelectric materials",
  "771 thermoelectric materials with synthesis recipes",
  "Precursors, target thermoelectrics, synthesis operation sequences (synthesis graph) and process conditions.",
  "Precursor selection; infer synthesis routes; predict operation sequences/conditions; link thermoelectric properties.",
  [2,0,2,2,0,0],[2,2,2]),
 ("A-Lab experimental synthesis data", "2023", "Hybrid",
  "https://www.nature.com/articles/s41586-023-06734-w", "10.1038/s41586-023-06734-w", "Inorganic solids; oxides/phosphates",
  "17-day continuous run; 57 targets; 36 compounds synthesized",
  "Autonomous robotic synthesis with literature-inspired recipes, precursor selection, robot execution and XRD feedback that adapts subsequent experiments.",
  "Compute-screen candidates; propose recipes; robot execution; XRD characterization and result analysis.",
  [4,4,4,3,3,4],[2,2,2]),
 ("Open Materials Guide (OMG)", "2025", "Experimental",
  "https://doi.org/10.48550/arXiv.2502.16457", "10.48550/arXiv.2502.16457", "Diverse inorganic materials",
  "~17,667 records",
  "Synthesis recipes with raw materials, equipment, steps and characterization; AlchemyBench uses it for precursor/equipment/step/characterization prediction.",
  "Raw-material selection; synthesis-route generation; operation-step generation; characterization prediction.",
  [2,1,3,2,1,1],[2,2,2]),
 ("Inorganic synthesis recipes (Kononova text-mined subset)", "2025", "Experimental",
  "https://doi.org/10.1021/acsami.5c11229", "10.1021/acsami.5c11229", "Inorganic solid-state",
  "~18,804 filtered reactions; 1,000 test records per task",
  "Literature-mined solid-state recipes to evaluate LLM precursor recommendation, calcination and sintering temperature prediction.",
  "Predict precursors; predict calcination/sintering temperatures; supplement route raw-material/condition info.",
  [2,1,2,2,1,1],[2,2,1]),
 ("ZeoSyn", "2026", "Experimental",
  "https://doi.org/10.1038/s43588-025-00949-9", "10.1038/s43588-025-00949-9", "Zeolites (incl. UFI)",
  "23,000+ synthesis recipes",
  "Zeolite crystal structures with synthesis recipes; DiffSyn generates candidate routes from target structure + organic template, handling one-to-many structure-condition relations.",
  "Target structure/template selection; candidate route generation; synthesis conditions; experimental validation of generated routes.",
  [3,1,3,3,1,1],[2,2,1]),
 ("DDSE (Dynamic Database of Solid-State Electrolyte)", "2024", "Hybrid",
  "", "", "Oxides; sulfides; polymers",
  "2,000+ electrolyte entries",
  "Literature-extracted starting materials, synthesis operations and conditions for solid-state electrolytes.",
  "Provide raw-material, synthesis and modification references for target performance.",
  [2,0,2,2,0,0],[1,1,1]),
 ("OBELiX (experimental solid-state electrolyte dataset)", "2025", "Experimental",
  "https://github.com/NRC-Mila/OBELiX", "", "Oxides; sulfides; polymers",
  "~600 synthesized electrolytes with room-T measured ionic conductivity",
  "Experimentally synthesized solid-state electrolytes with measured room-temperature ionic conductivity and structural parameters.",
  "Provide composition/space-group structural references for modeling synthesis targets.",
  [1,0,1,1,0,0],[2,1,1]),
]

X_DIMS = ["O","A","I","G","U","P"]
Y_DIMS = ["E","R","C"]

def main():
    d = json.load(open(DATA, encoding="utf-8"))
    existing = {x["name"].lower() for x in d}
    added = 0
    for (name, year, dt, url, doi, mat, scale, desc, usage, xs, ys) in NEW:
        if name.lower() in existing:
            print("skip (exists):", name); continue
        scores = {dim: v for dim, v in zip(X_DIMS, xs)}
        scores.update({dim: v for dim, v in zip(Y_DIMS, ys)})
        comp = round(sum(xs + ys) / 9.0, 2)
        rec = {
            "name": name, "category": "Workflow & Data", "task_type": "Workflow & Data",
            "data_type": dt, "year": year, "url": url, "doi": doi,
            "material_system": mat, "scale": scale, "description": desc, "usage": usage,
            "bib": "", "baseline": "", "source_sheet": "路线与步骤规划",
            "score": comp,
            "agent_review": {"scores": scores, "evidence_source": "table",
                             "note": "Scored from online table evidence; static data resources capped A<=1,P<=1."},
        }
        d.append(rec)
        added += 1
        print(f"add: {name}  composite={comp}")
    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nAdded {added}; total now {len(d)}")

if __name__ == "__main__":
    main()