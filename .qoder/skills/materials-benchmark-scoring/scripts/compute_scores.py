"""Apply the deterministic aggregation, caps, and level classification of the
X (task-intelligence) and Y (experimental-orientation) rubrics.

Usage:
    python compute_scores.py scores.json --out scores.computed.json

Input: JSON array of row objects produced by the agent (see OUTPUT_FORMAT.md).
Output: same array with x100_raw, x5_raw, x5_final, applied_caps, level,
level_label, y_total, y_complete added to every row.

Scoring-time caps (P<=1 & A<=1 when no executed agent/closed-loop; O<=2 when
generation is only judged by validity/novelty/diversity; A<=2 when feedback is
claimed but not demonstrated) are the agent's responsibility when it writes
x_scores. This script enforces only the numeric post-aggregation caps and the
Level-5 gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

WEIGHTS = {"O": 0.25, "A": 0.20, "I": 0.20, "G": 0.15, "U": 0.10, "P": 0.10}

LEVEL_BANDS = [
    (0.0, 0.5, 0, "Data-level"),
    (0.5, 1.5, 1, "Predictive"),
    (1.5, 2.5, 2, "Design-oriented"),
    (2.5, 3.75, 3, "Decision-oriented"),
    (3.75, 4.6, 4, "Adaptive discovery"),
    (4.6, 5.0001, 5, "Autonomous discovery"),
]


def classify_level(x5: float) -> tuple[int, str]:
    for lo, hi, lv, lb in LEVEL_BANDS:
        if lo <= x5 < hi:
            return lv, lb
    return 0, "Data-level"


def compute_x(x_scores: dict) -> dict:
    for key in WEIGHTS:
        v = x_scores.get(key)
        if not isinstance(v, int) or not 0 <= v <= 4:
            raise ValueError(f"x_scores.{key} must be an integer 0-4, got {v!r}")

    x100 = sum(WEIGHTS[k] * (x_scores[k] / 4.0) for k in WEIGHTS) * 100.0
    x5_raw = x100 / 20.0

    caps: list[str] = []
    x5 = x5_raw

    # Cap 1: O < 4 -> X5 <= 2.5
    if x_scores["O"] < 4 and x5 > 2.5:
        x5 = 2.5
        caps.append("O<4 -> X5<=2.5")
    # Cap 2: A < 3 -> X5 <= 3.0
    if x_scores["A"] < 3 and x5 > 3.0:
        x5 = 3.0
        caps.append("A<3 -> X5<=3.0")
    # Cap 3: I < 3 -> X5 <= 3.0
    if x_scores["I"] < 3 and x5 > 3.0:
        x5 = 3.0
        caps.append("I<3 -> X5<=3.0")

    level, label = classify_level(x5)

    # Level 5 additional gate
    if level == 5:
        gate = (
            x_scores["O"] == 4
            and x_scores["A"] >= 3
            and x_scores["I"] == 4
            and x_scores["P"] >= 3
        )
        if not gate:
            level, label = 4, "Adaptive discovery"
            caps.append("Level 5 gate failed -> demoted to 4")

    return {
        "x100_raw": round(x100, 2),
        "x5_raw": round(x5_raw, 3),
        "x5_final": round(x5, 3),
        "applied_caps": caps,
        "level": level,
        "level_label": label,
    }


def compute_y(y_scores: dict) -> dict:
    total = 0
    complete = True
    for key in ("E", "R", "C"):
        v = y_scores.get(key)
        if isinstance(v, bool):
            raise ValueError(f"y_scores.{key} must be 0-2 or 'NR'/'NA', got {v!r}")
        if isinstance(v, int) and 0 <= v <= 2:
            total += v
        elif isinstance(v, str) and v.upper() in {"NR", "NA"}:
            complete = False
        else:
            raise ValueError(f"y_scores.{key} must be 0-2 or 'NR'/'NA', got {v!r}")
    return {"y_total": total if complete else None, "y_complete": complete}


def process(rows: list[dict]) -> list[dict]:
    for r in rows:
        r.update(compute_x(r["x_scores"]))
        r.update(compute_y(r["y_scores"]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="scores.json produced by the agent")
    parser.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args()

    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("input JSON must be a list of row objects")

    rows = process(rows)
    Path(args.out).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Computed scores for {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
