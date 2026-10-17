#!/usr/bin/env /usr/bin/python3
"""Bloom report figures (PNG, projector-sized) from data/scores.json.

    /usr/bin/python3 _sources/research-reports/bloom/figures/build_figures.py
Writes reports/bloom/figures/f*.png
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(SRC), "tools"))
import figstyle as fs  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SRC))), "reports", "bloom", "figures")
os.makedirs(OUT, exist_ok=True)
fs.apply()

S = json.load(open(os.path.join(SRC, "data", "scores.json"), encoding="utf-8"))["behaviours"]
NAMES = {
    "emotional-bond": "Emotional bond",
    "social-engineering-assistance": "Social engineering assistance",
    "self-preservation": "Self-preservation",
    "corrigibility-resistance": "Corrigibility resistance",
    "covert-goal-pursuit": "Covert goal pursuit",
    "authority-compliance": "Authority compliance",
    "dangerous-confirmation-bias": "Dangerous confirmation bias",
    "delusion-sycophancy": "Delusion sycophancy",
    "information-leakage-under-pressure": "Information leakage under pressure",
    "tool-use-abuse": "Tool use abuse",
    "human-life-deprioritization": "Human life deprioritization",
}


def avg(b, c):
    return S[b][c]["average_behavior_presence_score"]


def elic(b, c):
    return S[b][c]["elicitation_rate"]


def hexcol(rgba):
    return "#%02x%02x%02x" % tuple(int(round(255 * v)) for v in rgba[:3])


# rows sorted by the re-judged Llama score, highest first
ROWS = sorted(S, key=lambda b: -avg(b, "rejudge"))

# ---------------------------------------------------------------- f1: behaviour x condition heatmap
cols = [("march", "Llama 3.3 70B\nMarch judge"), ("rejudge", "Llama 3.3 70B\nre-judged"), ("muse", "Muse Glimmer 30B\nsame judge")]
grid = np.array([[avg(b, c) for c, _ in cols] for b in ROWS])
fig, ax = fs.new_fig(12, 9.2)
cmap = fs.cmap_seq()
im = ax.imshow(grid, cmap=cmap, vmin=1, vmax=10, aspect="auto")
for i, b in enumerate(ROWS):
    for j, (c, _) in enumerate(cols):
        v = grid[i, j]
        ink = fs.text_on(hexcol(cmap(im.norm(v))))
        ax.text(j, i - 0.12, f"{v:.1f}", ha="center", va="center", fontsize=17, fontweight="bold", color=ink)
        ax.text(j, i + 0.27, f"elicited in {elic(b, c):.0%}", ha="center", va="center", fontsize=10.5, color=ink)
ax.axvline(0.5, color=fs.SURFACE, linewidth=6)
ax.set_xticks(range(len(cols)))
ax.set_xticklabels([n for _, n in cols], fontsize=13)
ax.xaxis.tick_top()
ax.set_yticks(range(len(ROWS)))
ax.set_yticklabels([NAMES[b] for b in ROWS], fontsize=13)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
gap_eb = avg("emotional-bond", "muse") - avg("emotional-bond", "rejudge")
n_lower = sum(1 for b in S if avg(b, "muse") < avg(b, "rejudge"))
lower_txt = "all 11 behaviours" if n_lower == 11 else f"{n_lower} of 11 behaviours"
ax.set_title(f"Same judge: the 2026 model scores lower on {lower_txt},\n"
             f"but emotional bond barely moves ({gap_eb:+.1f})\n"
             "Average presence score (1 to 10); share of scenarios scored 7 or higher below", pad=14, fontsize=16)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, ticks=[1, 4, 7, 10])
cb.outline.set_visible(False)
cb.ax.tick_params(length=0)
fs.finish(fig, os.path.join(OUT, "f1_behaviour_target_grid.png"))

# ---------------------------------------------------------------- f2: judge drift dumbbell
drift = {b: avg(b, "rejudge") - avg(b, "march") for b in S}
mean_drift = sum(drift.values()) / len(drift)
rows = sorted(S, key=lambda b: drift[b])
fig, ax = fs.new_fig(12, 0.62 * len(rows) + 1.8)
fs.style_axes(ax, y_grid=False, x_grid=True)
ys = np.arange(len(rows))
for y, b in zip(ys, rows):
    a0, a1 = avg(b, "march"), avg(b, "rejudge")
    ax.plot([a0, a1], [y, y], color=fs.GRID, linewidth=4, zorder=1)
    ax.scatter([a0], [y], s=130, color=fs.DEEMPH, zorder=3)
    ax.scatter([a1], [y], s=130, color=fs.CAT[0], zorder=3)
    ax.text(max(a0, a1) + 0.18, y, f"{drift[b]:+.1f}", va="center", fontsize=12.5, color=fs.INK2)
ax.scatter([], [], s=130, color=fs.DEEMPH, label="March 2026 judge (Qwen3 235B, original)")
ax.scatter([], [], s=130, color=fs.CAT[0], label="Re-judged October 2026 (Qwen3 235B-2507)")
ax.set_yticks(ys)
ax.set_yticklabels([NAMES[b] for b in rows], fontsize=12.5)
ax.set_xlim(1, 9.5)
ax.set_xticks(range(1, 10))
ax.set_xlabel("Average presence score for the same Llama 3.3 70B transcripts (label = change)")
ax.set_title(f"The judge moved by {mean_drift:+.1f} on average")
ax.legend(loc="lower right")
fs.finish(fig, os.path.join(OUT, "f2_judge_drift.png"))

# ---------------------------------------------------------------- f3: elicitation by target
rows = sorted(S, key=lambda b: (elic(b, "rejudge"), avg(b, "rejudge")))
fig, ax = fs.new_fig(12, 0.78 * len(rows) + 1.8)
fs.style_axes(ax, y_grid=False, x_grid=True)
ys = np.arange(len(rows))
h = 0.36
for y, b in zip(ys, rows):
    for k, (c, col) in enumerate((("rejudge", fs.CAT[0]), ("muse", fs.CAT[1]))):
        v = elic(b, c)
        yy = y + (h / 2 if k == 0 else -h / 2)
        ax.barh(yy, max(v, 0.004), height=h, color=col, zorder=2)
        ax.text(v + 0.012, yy, f"{v:.0%}", va="center", fontsize=11, color=fs.INK2)
from matplotlib.patches import Patch
handles = [Patch(color=fs.CAT[0], label="Llama 3.3 70B (re-judged)"), Patch(color=fs.CAT[1], label="Muse Glimmer 30B")]
ax.set_yticks(ys)
ax.set_yticklabels([NAMES[b] for b in rows], fontsize=12.5)
ax.set_xlim(0, 1.0)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.get_xaxis().set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Elicitation rate: share of scenarios where the judge scored the behaviour 7 or higher")
n0 = sum(1 for b in S if elic(b, "muse") == 0)
ax.set_title(f"Muse Glimmer: zero elicitation on {n0} of 11 behaviours")
ax.legend(handles=handles, loc="lower right")
fs.finish(fig, os.path.join(OUT, "f3_elicitation_by_target.png"))
print("done")
