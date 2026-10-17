#!/usr/bin/env /usr/bin/python3
"""SelfJudge report figures (PNG, projector-sized) from data/models.json + data/metrics/*.json.

    /usr/bin/python3 _sources/research-reports/selfjudge/figures/build_figures.py
Writes reports/selfjudge/figures/f*.png
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(SRC), "tools"))
import figstyle as fs  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SRC))), "reports", "selfjudge", "figures")
os.makedirs(OUT, exist_ok=True)
fs.apply()

models = json.load(open(os.path.join(SRC, "data", "models.json"), encoding="utf-8"))
metrics = {m["dir"]: json.load(open(os.path.join(SRC, "data", "metrics", m["dir"] + ".json"), encoding="utf-8"))
           for m in models}
open_models = [m for m in models if not m["closed"] and m["params_b"]]
ceiling = [m for m in models if m["closed"]]
RUN_COLOR = {"2026-07": fs.CAT[0], "2026-10": fs.CAT[1]}
RUN_LABEL = {"2026-07": "July 2026 run", "2026-10": "October 2026 run"}
SHORT = {  # short labels for crowded charts
    "Nemotron 3 Nano (MoE)": "Nemotron 3 Nano", "Gemma 4 26B-A4B (MoE)": "Gemma 4 26B-A4B",
    "LFM2.5 24B-A2B (MoE)": "LFM2.5 24B-A2B", "Nemotron 3.5 Lightning (MoE)": "Nemotron 3.5 Lightning",
    "GPT-6 Luna (closed, ceiling)": "GPT-6 Luna",
}


def short(m):
    return SHORT.get(m["display_name"], m["display_name"])


def ci_err(m, key="anchors"):
    o = metrics[m["dir"]]["overall"]
    blk = o[key] if key == "anchors" else o
    lo, hi = blk["accuracy_ci"]
    return blk["accuracy"] - lo, hi - blk["accuracy"]


def label_points(ax, xs, ys, names, dx=0.03, dy=0.0, size=11, ha="left"):
    for x, y, n in zip(xs, ys, names):
        ax.annotate(n, (x, y), xytext=(6, dy), textcoords="offset points", fontsize=size,
                    color=fs.INK2, ha=ha, va="center")


# ---------------------------------------------------------------- f1: judging skill vs params
fig, ax = fs.new_fig()
fs.style_axes(ax)
ax.axhline(0.5, color=fs.MUTED, linestyle=(0, (4, 4)), linewidth=1.5)
ax.text(0.72, 0.505, "50% = coin flip (and also 'always say PASS')", fontsize=12, color=fs.MUTED, va="bottom")
for c in ceiling:
    y = c["anchor_accuracy"]
    ax.axhline(y, color=fs.INK2, linestyle=(0, (2, 3)), linewidth=1.5)
    ax.text(0.72, y - 0.008, f"{short(c)}, closed model, not on device: {y:.0%}", fontsize=12, color=fs.INK2, va="top")
for run in ("2026-07", "2026-10"):
    for moe in (False, True):
        pts = [m for m in open_models if m["run"] == run and m["moe"] == moe]
        if not pts:
            continue
        xs = [m["params_b"] for m in pts]
        ys = [m["anchor_accuracy"] for m in pts]
        err = np.array([ci_err(m) for m in pts]).T
        ax.errorbar(xs, ys, yerr=err, fmt="none", ecolor=RUN_COLOR[run], elinewidth=1.2, capsize=3, alpha=0.6)
        ax.scatter(xs, ys, s=110, facecolors="white" if moe else RUN_COLOR[run], edgecolors=RUN_COLOR[run],
                   linewidths=2, zorder=3, label=f"{RUN_LABEL[run]}{', MoE (active params)' if moe else ''}")
ax.set_xscale("log")
ax.set_xticks([1, 2, 3, 5, 8, 14, 27, 70])
ax.get_xaxis().set_major_formatter(lambda v, _: f"{v:g}B")
ax.set_xlim(0.7, 160)
ax.set_ylim(0.35, 1.03)
ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.get_yaxis().set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Parameters (billions, active parameters for MoE models), log scale")
ax.set_ylabel("Judging skill: accuracy on planted anchors (95% CI)")
ax.set_title("Judging skill switches on around 3B and then stops improving")
ax.legend(loc="lower right")
fs.place_labels(ax, [(m["params_b"], m["anchor_accuracy"], short(m)) for m in open_models], x_group=170, min_gap=17)
fs.finish(fig, os.path.join(OUT, "f1_skill_vs_params.png"))

# ---------------------------------------------------------------- f2: judging skill vs release month
fig, ax = fs.new_fig()
fs.style_axes(ax)
ax.axhline(0.5, color=fs.MUTED, linestyle=(0, (4, 4)), linewidth=1.5)
def month(s):
    y, mth = s.split("-")
    return dt.date(int(y), int(mth), 15)
pts = [m for m in models if m["release"]]
for m in pts:
    x = month(m["release"])
    y = m["anchor_accuracy"]
    if m["closed"]:
        ax.scatter([x], [y], s=160, marker="D", facecolors="white", edgecolors=fs.INK2, linewidths=2, zorder=3)
    else:
        size = 60 + 4.5 * m["params_b"]
        ax.scatter([x], [y], s=size, facecolors="white" if m["moe"] else fs.CAT[0], edgecolors=fs.CAT[0],
                   linewidths=2, zorder=3, alpha=0.9)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_xlim(dt.date(2024, 7, 1), dt.date(2027, 2, 1))
ax.set_ylim(0.35, 1.03)
ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.get_yaxis().set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Model release month (marker area grows with parameter count; hollow = MoE; diamond = closed model)")
ax.set_ylabel("Judging skill: accuracy on planted anchors")
ax.set_title("The time perspective: judging skill by model generation")
fs.place_labels(ax, [(mdates.date2num(month(m["release"])), m["anchor_accuracy"], short(m)) for m in pts], x_group=150, min_gap=17)
fs.finish(fig, os.path.join(OUT, "f2_skill_vs_release.png"))

# ---------------------------------------------------------------- f3: self-leniency vs params
fig, ax = fs.new_fig()
fs.style_axes(ax)
ax.axhline(0, color=fs.BASELINE, linewidth=1.5)
ax.text(0.72, 0.01, "0 = judges its own failures as strictly as planted ones", fontsize=12, color=fs.MUTED, va="bottom")
for run in ("2026-07", "2026-10"):
    pts = [m for m in open_models if m["run"] == run and m["self_leniency"] is not None]
    if not pts:
        continue
    big = [m for m in pts if (m.get("n_own_fail") or 0) >= 10]
    small = [m for m in pts if (m.get("n_own_fail") or 0) < 10]
    if big:
        ax.scatter([m["params_b"] for m in big], [m["self_leniency"] for m in big], s=110,
                   facecolors=[("white" if m["moe"] else RUN_COLOR[run]) for m in big], edgecolors=RUN_COLOR[run],
                   linewidths=2, zorder=3, label=RUN_LABEL[run])
    if small:
        ax.scatter([m["params_b"] for m in small], [m["self_leniency"] for m in small], s=110, marker="x",
                   color=RUN_COLOR[run], linewidths=2, zorder=3,
                   label=f"{RUN_LABEL[run]}, fewer than 10 own failures (unreliable)")
for c in ceiling:
    if c["self_leniency"] is not None:
        ax.axhline(c["self_leniency"], color=fs.INK2, linestyle=(0, (2, 3)), linewidth=1.5)
        ax.text(0.72, c["self_leniency"] + 0.01, f"{short(c)} (closed): {c['self_leniency']:+.2f}", fontsize=12, color=fs.INK2)
ax.set_xscale("log")
ax.set_xticks([1, 2, 3, 5, 8, 14, 27, 70])
ax.get_xaxis().set_major_formatter(lambda v, _: f"{v:g}B")
ax.set_xlim(0.7, 160)
ax.set_ylim(-0.15, 1.05)
ax.set_xlabel("Parameters (billions, active for MoE), log scale")
ax.set_ylabel("Self-leniency = own-failure miss rate minus planted-failure miss rate")
ax.set_title("Every model misses more of its own failures than of planted ones")
ax.legend(loc="upper right", fontsize=11)
fs.place_labels(ax, [(m["params_b"], m["self_leniency"], short(m)) for m in open_models if m["self_leniency"] is not None], x_group=120, min_gap=17)
fs.finish(fig, os.path.join(OUT, "f3_self_leniency_vs_params.png"))

# ---------------------------------------------------------------- f4: self-assessment vs judging skill (dumbbell)
rows = sorted([m for m in models if m["params_b"] or m["closed"]], key=lambda m: (m["closed"], m["params_b"] or 0))
fig, ax = fs.new_fig(12, 0.42 * len(rows) + 1.6)
fs.style_axes(ax, y_grid=False, x_grid=True)
ys = np.arange(len(rows))[::-1]
for y, m in zip(ys, rows):
    a, s = m["anchor_accuracy"], m["self_accuracy"]
    ax.plot([s, a], [y, y], color=fs.GRID, linewidth=3, zorder=1)
    ax.scatter([a], [y], s=120, color=fs.CAT[0], zorder=3)
    ax.scatter([s], [y], s=120, color=fs.CAT[1], zorder=3)
    ax.text(max(a, s) + 0.012, y, f"{a - s:+.0%}", va="center", fontsize=11, color=fs.INK2)
ax.scatter([], [], s=120, color=fs.CAT[0], label="judging skill (planted anchors)")
ax.scatter([], [], s=120, color=fs.CAT[1], label="self-assessment (own outputs)")
ax.set_yticks(ys)
ax.set_yticklabels([f"{short(m)}  ·  {'closed' if m['closed'] else str(m['params_b']).rstrip('0').rstrip('.') + 'B'}" for m in rows], fontsize=12)
ax.set_xlim(0.3, 1.08)
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.get_xaxis().set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Accuracy (gap label = judging skill minus self-assessment)")
ax.set_title("Grading planted answers is easier than grading your own")
ax.legend(loc="lower left")
fs.finish(fig, os.path.join(OUT, "f4_self_vs_anchors.png"))

# ---------------------------------------------------------------- f5: category heatmap (anchors)
cats = ["factual_grounding", "instruction_following", "safety_boundary", "consistency", "tone_appropriateness"]
cat_names = ["Factual\ngrounding", "Instruction\nfollowing", "Safety\nboundary", "Consistency", "Tone"]
grid = np.array([[metrics[m["dir"]]["categories"][c]["anchors"]["accuracy"] for c in cats] for m in rows])
fig, ax = fs.new_fig(12, 0.5 * len(rows) + 2.2)
im = ax.imshow(grid, cmap=fs.cmap_seq(), vmin=0.4, vmax=1.0, aspect="auto")
for i in range(len(rows)):
    for j in range(len(cats)):
        v = grid[i, j]
        ax.text(j, i, f"{v:.0%}", ha="center", va="center", fontsize=12,
                color=fs.text_on(im.cmap(im.norm(v)) and "#%02x%02x%02x" % tuple(int(255 * c) for c in im.cmap(im.norm(v))[:3])))
ax.set_xticks(range(len(cats)))
ax.set_xticklabels(cat_names, fontsize=12)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([short(m) for m in rows], fontsize=12)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("Judging skill by failure category (accuracy on planted anchors)")
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
cb.outline.set_visible(False)
fs.finish(fig, os.path.join(OUT, "f5_category_heatmap.png"))
print("done")
