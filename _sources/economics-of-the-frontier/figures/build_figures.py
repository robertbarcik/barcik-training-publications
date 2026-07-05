#!/usr/bin/env python3
"""
Figure builder for the booklet "The Economics of the Frontier".

Renders four static PNGs into economics-of-the-frontier/figures/.
Run:  python3 _sources/economics-of-the-frontier/figures/build_figures.py
Deps: matplotlib  (pip3 install matplotlib)

Design goal: mathematical accuracy and legibility. No interactivity.
All figures use the booklet's palette and a clean sans-serif look.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

# ── Palette (matches the booklet CSS) ──────────────────────────────
NAVY    = "#1e3a5f"
ACCENT  = "#3b82f6"
GREEN   = "#2D7A4F"
ORANGE  = "#E05A33"
PURPLE  = "#7C6DD8"
TEAL    = "#0d9488"
RED     = "#dc2626"
INK     = "#1e293b"
MUTE    = "#64748b"
LINE    = "#cbd5e1"
PAPER   = "#ffffff"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "text.color": INK,
    "axes.edgecolor": LINE,
    "axes.labelcolor": INK,
    "xtick.color": MUTE,
    "ytick.color": MUTE,
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                   "economics-of-the-frontier", "figures")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)
DPI = 200


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("wrote", path)


def box(ax, x, y, w, h, text, fc, ec, tc, fs=11, weight="normal", sub=None):
    """Rounded box centred at (x, y)."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.10",
                       fc=fc, ec=ec, lw=1.5, zorder=3)
    ax.add_patch(p)
    if sub:
        ax.text(x, y + h * 0.16, text, ha="center", va="center",
                fontsize=fs, fontweight=weight, color=tc, zorder=4)
        ax.text(x, y - h * 0.24, sub, ha="center", va="center",
                fontsize=fs - 2.5, color=tc, zorder=4)
    else:
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, fontweight=weight, color=tc, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# FIGURE 1 — How a lab works: money in, model, money out
# ═══════════════════════════════════════════════════════════════════
def fig_lab_economics():
    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # inputs
    box(ax, 2.1, 6.6, 3.0, 1.5, "A research team", PAPER, LINE, INK,
        fs=10.5, weight="bold", sub="salaries, for months")
    box(ax, 2.1, 3.1, 3.0, 1.5, "Compute", PAPER, LINE, INK,
        fs=10.5, weight="bold", sub="one long training run")

    # the model (one-time cost)
    box(ax, 7.4, 4.85, 3.6, 2.5, "ONE MODEL", NAVY, NAVY, PAPER,
        fs=13, weight="bold", sub="a one-time build cost")

    # arrows in
    for sy in (6.6, 3.1):
        ax.add_patch(FancyArrowPatch((3.65, sy), (5.55, 4.85),
                     arrowstyle="-|>", mutation_scale=16,
                     color=NAVY, lw=2, connectionstyle="arc3,rad=0.0", zorder=2))

    # revenue boxes
    rev = [
        (7.05, "Metered API", "billed per token used"),
        (4.55, "Subscriptions", "flat monthly plans"),
        (2.05, "Enterprise bundles", "seats + committed use"),
    ]
    for y, t, s in rev:
        box(ax, 13.0, y, 3.9, 1.7, t, "#f0fdfa", TEAL, INK,
            fs=10.5, weight="bold", sub=s)
        ax.add_patch(FancyArrowPatch((9.25, 4.85), (11.0, y),
                     arrowstyle="-|>", mutation_scale=15,
                     color=TEAL, lw=2, connectionstyle="arc3,rad=0.05", zorder=2))

    # serving-cost note
    ax.text(7.4, 2.75, "every answer it gives\nalso costs a little compute",
            ha="center", va="center", fontsize=8.3, style="italic", color="#9aa7b8")

    ax.text(2.1, 8.5, "WHAT IT COSTS TO BUILD", ha="center", fontsize=8.6,
            fontweight="bold", color=MUTE)
    ax.text(13.0, 8.5, "HOW IT IS SOLD", ha="center", fontsize=8.6,
            fontweight="bold", color=MUTE)
    save(fig, "fig-lab-economics.png")


# ═══════════════════════════════════════════════════════════════════
# FIGURE 2 — The vintage cascade (mathematically honest, log scale)
# ═══════════════════════════════════════════════════════════════════
def fig_vintage():
    years = ["2023", "2024", "2025", "2026"]
    cost = [0.1, 1.0, 10.0, 100.0]      # $B, training cost per model
    revenue = [0.2, 2.0, 20.0, 200.0]   # $B, ~2x lifetime revenue
    company = [-0.1, -0.8, -8.0, -80.0] # $B, company annual result

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 7.2),
                                   gridspec_kw={"height_ratios": [1.15, 1]})
    x = np.arange(len(years))
    w = 0.36

    # ── top: per-vintage, log scale ──
    ax1.bar(x - w/2, cost, w, color=NAVY, label="Training cost (one-time)")
    ax1.bar(x + w/2, revenue, w, color=GREEN, label="Lifetime revenue (≈ 2×)")
    ax1.set_yscale("log")
    ax1.set_ylim(0.05, 400)
    ax1.set_ylabel("US$ billion  (log scale)", fontsize=9.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels([y + " model" for y in years], fontsize=10)
    ax1.set_title("Each model, on its own:  revenue ≈ 2× its training cost",
                  fontsize=11.5, fontweight="bold", color=NAVY, pad=10)
    for i in range(len(years)):
        ax1.text(x[i]-w/2, cost[i]*1.15, f"${cost[i]:g}B", ha="center",
                 va="bottom", fontsize=8.3, color=NAVY)
        ax1.text(x[i]+w/2, revenue[i]*1.15, f"${revenue[i]:g}B", ha="center",
                 va="bottom", fontsize=8.6, color=GREEN, fontweight="bold")
    ax1.legend(frameon=False, fontsize=9, loc="upper left")
    ax1.spines[["top", "right"]].set_visible(False)

    # ── bottom: company annual result, symlog ──
    ax2.bar(x, company, 0.5, color=RED)
    ax2.axhline(0, color=LINE, lw=1.2)
    ax2.set_yscale("symlog", linthresh=0.1)
    ax2.set_ylim(-300, 1)
    ax2.set_ylabel("US$ billion  (symlog scale)", fontsize=9.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels([y for y in years], fontsize=10)
    ax2.set_title("The same years, company-wide:  an accelerating loss",
                  fontsize=11.5, fontweight="bold", color=NAVY, pad=10)
    for i in range(len(years)):
        ax2.text(x[i], company[i]*1.35, f"−${abs(company[i]):g}B",
                 ha="center", va="top", fontsize=8.6, color=RED, fontweight="bold")
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.tick_params(axis="y", labelsize=8)

    fig.text(0.5, 0.005,
             "Stylised illustration of Dario Amodei’s framing, not Anthropic’s "
             "accounts. Every year the company finances a successor ≈ 10× larger.",
             ha="center", fontsize=8, style="italic", color=MUTE)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    save(fig, "fig-vintage.png")


# ═══════════════════════════════════════════════════════════════════
# FIGURE 3 — Revenue run-rate trajectories
# ═══════════════════════════════════════════════════════════════════
def fig_revenue():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    anthropic = [(2024.00, 0.1), (2024.92, 1), (2025.92, 9),
                 (2026.08, 14), (2026.17, 19), (2026.25, 30), (2026.42, 47)]
    openai = [(2024.00, 1.6), (2024.92, 4), (2025.92, 20), (2026.25, 24)]

    for data, color, name in [(anthropic, ACCENT, "Anthropic"),
                              (openai, ORANGE, "OpenAI")]:
        xs = [p[0] for p in data]
        ys = [p[1] for p in data]
        ax.plot(xs, ys, "-o", color=color, lw=2.6, ms=6.5,
                mfc=PAPER, mec=color, mew=2.2, label=name)
        ax.annotate(f"  {name}\n  ${ys[-1]:g}B", (xs[-1], ys[-1]),
                    fontsize=9.5, fontweight="bold", color=color, va="center")

    ax.set_xlim(2023.85, 2026.85)
    ax.set_ylim(0, 52)
    ax.set_xticks([2024, 2025, 2026])
    ax.set_xticklabels(["2024", "2025", "2026"], fontsize=10)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels(["$0B", "$10B", "$20B", "$30B", "$40B", "$50B"], fontsize=9)
    ax.set_ylabel("Annualised revenue run rate", fontsize=9.5)
    ax.set_title("Two run rates, two trajectories",
                 fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.grid(axis="y", color="#eef2f6", lw=1)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(2023.9, -10.0,
            "Run rate = the trailing month, annualised (labs use ×12 or ×13 mechanics). "
            "Recognised (GAAP) revenue is roughly half of each figure shown. "
            "Last point: $47B, late May 2026.",
            fontsize=8, style="italic", color=MUTE)
    save(fig, "fig-revenue.png")


# ═══════════════════════════════════════════════════════════════════
# FIGURE 4 — The circular flow (conceptual ring; deal figures live in
# an HTML table next to the figure in the booklet)
# ═══════════════════════════════════════════════════════════════════
def fig_circular():
    fig, ax = plt.subplots(figsize=(8.0, 6.4))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13)
    ax.set_aspect("equal")
    ax.axis("off")

    cx, cy = 8.0, 6.4
    # four stations, clockwise from top
    stations = [
        (cx, cy + 3.5, "1", "A hyperscaler invests\nequity in a lab", PURPLE, "#f3f1fc"),
        (cx + 4.6, cy, "2", "The lab now\nholds the cash", NAVY, PAPER),
        (cx, cy - 3.5, "3", "The lab spends it on the\nhyperscaler's compute", TEAL, "#f0fdfa"),
        (cx - 4.6, cy, "4", "The hyperscaler books\nit as its own revenue", NAVY, PAPER),
    ]
    pos = [(s[0], s[1]) for s in stations]
    for x, y, num, text, col, fc in stations:
        box(ax, x, y, 4.0, 1.7, "", fc, col, INK)
        ax.text(x, y + 0.42, "STEP " + num, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=col)
        ax.text(x, y - 0.22, text, ha="center", va="center",
                fontsize=9.4, color=INK, linespacing=1.4)

    # clockwise arrows along the ring
    for i in range(4):
        a = pos[i]
        b = pos[(i + 1) % 4]
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>",
                     mutation_scale=20, color="#94a3b8", lw=2.6,
                     connectionstyle="arc3,rad=-0.32", zorder=1,
                     shrinkA=34, shrinkB=34))

    # centre
    ax.text(cx, cy + 0.45, "$1", ha="center", va="center",
            fontsize=30, fontweight="bold", color=NAVY)
    ax.text(cx, cy - 0.85, "the same dollar:\ninvestment and revenue at once",
            ha="center", va="center", fontsize=8.6, style="italic",
            color=MUTE, linespacing=1.4)
    save(fig, "fig-circular.png")


if __name__ == "__main__":
    fig_lab_economics()
    fig_vintage()
    fig_revenue()
    fig_circular()
    print("done.")
