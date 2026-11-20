#!/usr/bin/env python3
"""Generate the two main figures of the materials-AI benchmark survey.

Fig 1: two-axis scoring framework (rubric schematic, data-independent).
Fig 2: quantitative map of scored benchmarks: intelligence X5 vs experimental
       preparation guidance S, coloured by task family (sheet).

Data source: summary/scored/*.computed.json (one file per sheet). The script is
incremental: sheets scored later are picked up automatically on re-run.

Outputs (PNG 300 dpi + vector PDF) into summary/figures/.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent
SCORED = ROOT / "scored"
OUT = ROOT / "figures"

# ---------------------------------------------------------------- palette ---
BLUE = "#3E7CBF"        # intelligence axis / property prediction family
BLUE_LT = "#EAF2FB"
GREEN = "#2E9E7E"       # experimental axis / inverse design family
GREEN_LT = "#EAF6F0"
ORANGE = "#EE7E3F"      # iterative optimisation / closed-loop family
PURPLE = "#7B5EA7"      # frontier / ecosystem
PURPLE_LT = "#F3EDFA"
INK = "#1F3864"
GREY = "#5A6472"

FAMILY = {
    "性质预测（正向）": ("Property prediction", BLUE),
    "逆向设计": ("Generation / inverse design", GREEN),
    "迭代优化（时序）": ("Iterative optimisation / closed-loop", ORANGE),
}
LEVEL_BANDS = [  # (label, lo, hi, short description)
    ("L0", 0.0, 0.5, "symbolic"),
    ("L1", 0.5, 1.5, "static fitting"),
    ("L2", 1.5, 2.5, "constrained task solving"),
    ("L3", 2.5, 3.75, "structured reasoning"),
    ("L4", 3.75, 4.6, "agent-grade intelligence"),
    ("L5", 4.6, 5.0, "scientific discovery"),
]
LEVEL_TINT = ["#F7FAFD", "#EDF3FA"]


# ------------------------------------------------------------------ data ---
def load_rows():
    rows = []
    for f in sorted(SCORED.glob("*.computed.json")):
        sheet = f.name[: -len(".computed.json")]
        label, color = FAMILY.get(sheet, (sheet, GREY))
        for r in json.loads(f.read_text(encoding="utf-8")):
            r = dict(r)
            r["sheet"] = sheet
            r["family"] = label
            r["color"] = color
            rows.append(r)
    return rows


def box(ax, x, y, w, h, fc, ec=None, lw=1.0, rounding=0.6, z=1):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.15,rounding_size={rounding}",
        fc=fc, ec=ec or fc, lw=lw, zorder=z,
    )
    ax.add_patch(p)
    return p


def arrow(ax, x0, y0, x1, y1, color=GREY, lw=1.4, style="-|>", z=3):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12,
        color=color, lw=lw, zorder=z, shrinkA=1, shrinkB=1,
    ))


# ------------------------------------------------------------- figure 1 ----
def fig1_framework():
    fig, ax = plt.subplots(figsize=(13.6, 7.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 97.2, "Two-axis evaluation framework for materials AI benchmarks",
            ha="center", va="center", fontsize=15, fontweight="bold", color=INK)
    ax.text(50, 93.6, "Axis X: task intelligence (what the model must do)   ·   "
                      "Axis Y: experimental preparation guidance (how close to the real lab)",
            ha="center", va="center", fontsize=9.5, color=GREY)

    # ---- X zone -----------------------------------------------------------
    box(ax, 2, 24.5, 54.5, 66.5, BLUE_LT, ec=BLUE, lw=1.2, rounding=1.2, z=0)
    ax.text(29.2, 88.2, "AXIS X · TASK INTELLIGENCE", ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=BLUE)
    dims = [
        ("O", "Open-endedness", "25%", "open, non-enumerable output space"),
        ("A", "Autonomy", "20%", "one-shot assistance → full autonomy"),
        ("I", "Iteration & feedback", "20%", "single shot → long-horizon loop"),
        ("G", "Generalisation", "15%", "transfer across systems / domains"),
        ("U", "Uncertainty", "10%", "calibrated, decision-used uncertainty"),
        ("P", "Process & executability", "10%", "executable, reusable artifacts"),
    ]
    for i, (sym, name, w, desc) in enumerate(dims):
        cx = 4.2 + (i % 2) * 25.6
        cy = 78.6 - (i // 2) * 9.6
        box(ax, cx, cy, 24.4, 8.4, "white", ec=BLUE, lw=0.9, z=2)
        ax.text(cx + 1.1, cy + 5.9, f"{sym} · {name}", fontsize=8.2,
                fontweight="bold", color=INK, va="center", zorder=3)
        ax.text(cx + 23.3, cy + 5.9, w, fontsize=8.2, fontweight="bold",
                color=BLUE, va="center", ha="right", zorder=3)
        ax.text(cx + 1.1, cy + 2.5, f"scored 0–4 · {desc}", fontsize=6.6,
                color=GREY, va="center", zorder=3)

    box(ax, 4.2, 48.4, 50.0, 8.6, "white", ec=BLUE, lw=0.9, z=2)
    ax.text(29.2, 54.6, r"$X_{100}=\sum_d w_d\cdot\frac{s_d}{4}\cdot100$"
            r"$\qquad X_5 = X_{100}/20 \in [0,5]$",
            ha="center", va="center", fontsize=9.2, color=INK, zorder=3)
    ax.text(29.2, 50.7, "weights  w = (25, 20, 20, 15, 10, 10) %  for (O, A, I, G, U, P)",
            ha="center", va="center", fontsize=7.0, color=GREY, zorder=3)

    box(ax, 4.2, 36.0, 50.0, 10.6, "white", ec=BLUE, lw=0.9, z=2)
    ax.text(5.2, 44.4, "Mandatory caps (anti-inflation)", fontsize=7.6,
            fontweight="bold", color=BLUE, va="center", zorder=3)
    caps = ("• no executed agent / closed loop  →  P ≤ 1, A ≤ 1\n"
            "• generation judged by validity / novelty / diversity only  →  O ≤ 2, X5 ≤ 2.5\n"
            "• after aggregation:  O < 4 → X5 ≤ 2.5 ·  A < 3 → X5 ≤ 3.0 ·  I < 3 → X5 ≤ 3.0")
    ax.text(5.2, 40.0, caps, fontsize=6.7, color=GREY, va="center", zorder=3,
            linespacing=1.5)

    # level ladder (inside the X panel)
    ax.text(4.2, 33.4, "Intelligence levels (X5)", fontsize=8.4,
            fontweight="bold", color=INK, va="center")
    x0, total_w = 4.2, 50.0
    span = [b[2] - b[1] for b in LEVEL_BANDS]
    ramp = ["#DCE6F2", "#BFD3EA", "#9DBEE0", "#74A3D2", "#4A83C4", "#2F5F9E"]
    for (lab, lo, hi, desc), w_, c in zip(LEVEL_BANDS, span, ramp):
        w = w_ / 5.0 * total_w
        ax.add_patch(Rectangle((x0, 26.6), w, 4.6, fc=c, ec="white", lw=1.0, zorder=2))
        ax.text(x0 + w / 2, 29.8, lab, ha="center", va="center", fontsize=7.6,
                fontweight="bold", color="white" if c in ramp[2:] else INK, zorder=3)
        ax.text(x0 + w / 2, 27.7, f"{lo:g}–{hi:g}", ha="center", va="center",
                fontsize=6.0, color="white" if c in ramp[2:] else INK, zorder=3)
        x0 += w
    ax.text(29.2, 25.5, "L5 gate: O = 4, A ≥ 3, I = 4, P ≥ 3", fontsize=6.6,
            color=GREY, va="center", ha="center")

    # ---- Y zone -----------------------------------------------------------
    box(ax, 60, 24.5, 38, 66.5, GREEN_LT, ec=GREEN, lw=1.2, rounding=1.2, z=0)
    ax.text(79, 88.2, "AXIS Y · EXPERIMENTAL PREPARATION",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color=GREEN)
    ydims = [
        ("E", "Experimental grounding", "0 computational only · 1 literature-derived data · 2 new experiments"),
        ("R", "Real-world realism", "0 in-silico · 1 surrogate of real conditions · 2 real-world constraints"),
        ("C", "Closed-loop readiness", "0 offline prediction · 1 human-in-the-loop · 2 autonomous closed loop"),
    ]
    for i, (sym, name, anch) in enumerate(ydims):
        cy = 78.6 - i * 9.6
        box(ax, 62, cy, 34, 8.4, "white", ec=GREEN, lw=0.9, z=2)
        ax.text(63.1, cy + 5.9, f"{sym} · {name}", fontsize=8.2,
                fontweight="bold", color=INK, va="center", zorder=3)
        ax.text(94.9, cy + 5.9, "0–2", fontsize=8.2, fontweight="bold",
                color=GREEN, va="center", ha="right", zorder=3)
        ax.text(63.1, cy + 2.5, anch, fontsize=6.6, color=GREY, va="center", zorder=3)

    box(ax, 62, 48.4, 34, 8.6, "white", ec=GREEN, lw=0.9, z=2)
    ax.text(79, 54.0, r"$S = E + R + C \in [0,6]$", ha="center", va="center",
            fontsize=10.0, color=INK, zorder=3)
    ax.text(79, 50.6, "experimental orientation of the benchmark",
            ha="center", va="center", fontsize=7.0, color=GREY, zorder=3)

    box(ax, 62, 36.0, 34, 10.6, "white", ec=GREEN, lw=0.9, z=2)
    ax.text(63.0, 44.4, "Missing-data rule", fontsize=7.6, fontweight="bold",
            color=GREEN, va="center", zorder=3)
    ax.text(63.0, 40.0,
            "a dimension marked NR / NA is never imputed:\n"
            "S is reported as not reportable and the benchmark\n"
            "is drawn in the dedicated strip of the map (Fig. 2)",
            fontsize=6.7, color=GREY, va="center", zorder=3, linespacing=1.5)
    ax.text(79, 30.6, "reading S:   0–2 computation-oriented   ·   3–4 literature /\n"
                      "hybrid grounding   ·   5–6 experiment-grounded closed loop",
            ha="center", va="center", fontsize=6.9, color=GREEN, zorder=3,
            linespacing=1.5)

    # ---- pipeline strip ---------------------------------------------------
    steps = [
        ("Online benchmark sheet\n(kdocs · 3 task-family tabs)", BLUE_LT, BLUE),
        ("Evidence gathering\nfull text first, table fields fallback", BLUE_LT, BLUE),
        ("Per-dimension scores\nevidence-only + confidence", "#F2F4F8", GREY),
        ("Deterministic aggregation\nweights · caps · levels · S", "#F2F4F8", GREY),
        ("Two-axis map + registry\nincremental, reproducible", PURPLE_LT, PURPLE),
    ]
    bw, bh, y = 17.6, 10.5, 8.0
    xs = [2.5, 22.4, 42.3, 62.2, 82.1]
    for (txt, fc, ec), x in zip(steps, xs):
        box(ax, x, y, bw, bh, fc, ec=ec, lw=1.0, z=2)
        ax.text(x + bw / 2, y + bh / 2, txt, ha="center", va="center",
                fontsize=7.2, color=INK, zorder=3, linespacing=1.4)
    for x in xs[:-1]:
        arrow(ax, x + bw + 0.4, y + bh / 2, x + bw + 2.0, y + bh / 2)
    ax.text(50, 3.2, "Every score is justified by quoted evidence; aggregation is "
                     "computed by script, never by hand.",
            ha="center", va="center", fontsize=7.4, style="italic", color=GREY)

    # connectors zones -> pipeline
    arrow(ax, 29.2, 24.1, 29.2, 19.2, color=BLUE, lw=1.2)
    arrow(ax, 79.0, 24.1, 79.0, 19.2, color=GREEN, lw=1.2)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "fig1_scoring_framework.png", dpi=300, bbox_inches="tight",
                facecolor="white")
    fig.savefig(OUT / "fig1_scoring_framework.pdf", bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------- figure 2 ----
def fig2_map(rows):
    complete = [r for r in rows if r.get("y_complete") and r.get("y_total") is not None]
    partial = [r for r in rows if r not in complete]
    families = []
    for r in rows:
        if r["family"] not in families:
            families.append(r["family"])
    fcolor = {r["family"]: r["color"] for r in rows}

    fig = plt.figure(figsize=(12.6, 8.4))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.24, 1.0, 0.15],
                          hspace=0.06, top=0.90, bottom=0.13, left=0.085, right=0.975)
    ax_top = fig.add_subplot(gs[0], sharex=None)
    ax = fig.add_subplot(gs[1])
    ax_rug = fig.add_subplot(gs[2])

    # level bands + frontier
    for i, (lab, lo, hi, desc) in enumerate(LEVEL_BANDS):
        ax.axvspan(lo, hi, color=LEVEL_TINT[i % 2], zorder=0)
        ax.text((lo + hi) / 2, 6.42, f"{lab} · {desc}", ha="center", va="bottom",
                fontsize=6.8, color=GREY, zorder=1)
        ax_top.axvspan(lo, hi, color=LEVEL_TINT[i % 2], zorder=0)
    ax.axvline(3.75, color=PURPLE, ls=":", lw=1.0, zorder=1)
    ax.add_patch(FancyBboxPatch(
        (3.78, 4.55), 1.18, 1.75, boxstyle="round,pad=0.05,rounding_size=0.12",
        fc=PURPLE_LT, ec=PURPLE, ls="--", lw=1.2, zorder=1))
    ax.text(4.37, 5.42, "emerging frontier:\nagent-grade intelligence\n+ experiment-grounded\nclosed loop",
            ha="center", va="center", fontsize=7.0, color=PURPLE,
            fontweight="bold", zorder=4, linespacing=1.35)

    # points
    for fam in families:
        sub = [r for r in complete if r["family"] == fam]
        ax.scatter([r["x5_final"] for r in sub], [r["y_total"] for r in sub],
                   s=86, c=fcolor[fam], edgecolors="white", lw=1.0,
                   label=fam, zorder=3, alpha=0.92)
        subp = [r for r in partial if r["family"] == fam]
        if subp:
            ax_rug.scatter([r["x5_final"] for r in subp], [0.5] * len(subp),
                           s=64, facecolors="none", edgecolors=fcolor[fam],
                           lw=1.3, zorder=3)

    # annotations of representative benchmarks
    notable = ["MADE", "MatFormBench", "MOCLIP", "CrystalGym", "Tartarus", "CSP"]
    picks = []
    for fam in families:
        sub = sorted([r for r in complete if r["family"] == fam],
                     key=lambda r: -r["x5_final"])[:2]
        picks.extend(sub)
    for r in complete:
        if any(k.lower() in (r.get("benchmark_name") or r.get("title") or "").lower()
               for k in notable) and r not in picks:
            picks.append(r)
    offs = [(9, 9), (-9, 11), (11, -9), (-11, -11), (13, 3), (-13, 5), (7, -13), (-7, 14)]
    for i, r in enumerate(picks[:10]):
        name = r.get("benchmark_name") or r.get("title") or ""
        name = name if len(name) <= 26 else name[:24] + "…"
        dx, dy = offs[i % len(offs)]
        ax.annotate(name, (r["x5_final"], r["y_total"]), textcoords="offset points",
                    xytext=(dx, dy), fontsize=6.6, color=INK, zorder=5,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=GREY, alpha=0.7))

    ax.set_ylim(-0.35, 6.55)
    ax.set_xlim(0, 5)
    ax.set_yticks(range(0, 7))
    ax.set_ylabel("Experimental preparation guidance  S = E + R + C  (0–6)",
                  fontsize=9.5, color=INK)
    ax.grid(axis="y", color="white", lw=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xticklabels([])

    # top marginal: level counts per family
    counts = {fam: [0] * len(LEVEL_BANDS) for fam in families}
    for r in rows:
        for i, (lab, lo, hi, _) in enumerate(LEVEL_BANDS):
            if lo <= r["x5_final"] < hi or (i == 5 and r["x5_final"] == 5):
                counts[r["family"]][i] += 1
                break
    bottoms = [0.0] * len(LEVEL_BANDS)
    for fam in families:
        vals = counts[fam]
        ax_top.bar([ (b[1] + b[2]) / 2 for b in LEVEL_BANDS ], vals,
                   width=[(b[2] - b[1]) * 0.72 for b in LEVEL_BANDS],
                   bottom=bottoms, color=fcolor[fam], edgecolor="white",
                   lw=0.8, label=fam, zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax_top.set_xlim(0, 5)
    ax_top.tick_params(labelbottom=False, labelsize=7)
    ax_top.set_ylabel("benchmarks\nper level", fontsize=7.6, color=GREY)
    for s in ("top", "right"):
        ax_top.spines[s].set_visible(False)
    ax_top.set_title("Quantitative landscape of materials AI benchmarks: "
                     "task intelligence vs experimental preparation guidance",
                     fontsize=13.5, fontweight="bold", color=INK, pad=10)

    # rug: not-reportable S
    ax_rug.set_xlim(0, 5)
    ax_rug.set_ylim(0, 1)
    ax_rug.set_yticks([])
    ax_rug.set_xticks([0, 1, 2, 3, 4, 5])
    ax_rug.set_xlabel("Final intelligence score  X5  (0–5)", fontsize=9.5, color=INK)
    ax_rug.text(0.02, 0.5, "S not reportable (NR/NA)", transform=ax_rug.transAxes,
                fontsize=7.0, color=GREY, va="center", ha="left", zorder=4)
    for s in ("top", "right", "left"):
        ax_rug.spines[s].set_visible(False)

    # legend + take-home banner
    handles, labels = ax.get_legend_handles_labels()
    from matplotlib.lines import Line2D
    handles.append(Line2D([0], [0], marker="o", color="none", markerfacecolor="none",
                          markeredgecolor=GREY, markersize=8,
                          label="open marker: S not reportable (NR/NA)"))
    fig.legend(handles=handles, loc="lower center", ncol=len(handles),
               bbox_to_anchor=(0.5, 0.055), fontsize=8, frameon=False)

    n = len(rows)
    n_front = sum(1 for r in complete if r["x5_final"] >= 3.75 and r["y_total"] >= 5)
    low = sum(1 for r in complete if r["level"] <= 2)
    pct = 100.0 * low / max(1, len(complete))
    msg = (f"{n} scored benchmarks across {len(families)} task family(ies):  "
           f"{pct:.0f}% of reportable-S benchmarks remain at or below Level-2 intelligence, and only "
           f"{n_front} couple agent-grade intelligence (L4–L5) with experiment-grounded closed loops (S ≥ 5).")
    if len(msg) > 150:
        cut = msg.rfind(" ", 0, 150)
        msg = msg[:cut] + "\n" + msg[cut + 1:]
    fig.text(0.5, 0.015, msg, ha="center", va="center", fontsize=8.4,
             fontweight="bold", color=INK, linespacing=1.4,
             bbox=dict(fc=BLUE_LT, ec=BLUE, lw=0.8, boxstyle="round,pad=0.5"))

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "fig2_intelligence_experiment_map.png", dpi=300,
                facecolor="white")
    fig.savefig(OUT / "fig2_intelligence_experiment_map.pdf", facecolor="white")
    plt.close(fig)


def main():
    rows = load_rows()
    print(f"loaded {len(rows)} scored rows from {SCORED}")
    fig1_framework()
    fig2_map(rows)
    print("wrote:", ", ".join(p.name for p in sorted(OUT.iterdir())))


if __name__ == "__main__":
    main()
