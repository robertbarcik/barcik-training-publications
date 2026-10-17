#!/usr/bin/env /usr/bin/python3
"""GeoBias report figures (PNG, projector-sized) from data/run_2026_03.json, data/run_2026_10.json
and data/models.json.

    /usr/bin/python3 _sources/research-reports/geobias/figures/build_figures.py
Writes reports/geobias/figures/f*.png
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(SRC), "tools"))
import figstyle as fs  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SRC))), "reports", "geobias", "figures")
os.makedirs(OUT, exist_ok=True)
fs.apply()

DATA = os.path.join(SRC, "data")
RUNS = {
    "run_2026_03": json.load(open(os.path.join(DATA, "run_2026_03.json"), encoding="utf-8")),
    "run_2026_10": json.load(open(os.path.join(DATA, "run_2026_10.json"), encoding="utf-8")),
}
MODELS = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))
RUN_COLOR = {"run_2026_03": fs.CAT[0], "run_2026_10": fs.CAT[1]}
RUN_LABEL = {"run_2026_03": "March 2026 run", "run_2026_10": "October 2026 run"}
RUN_SHORT = {"run_2026_03": "Mar", "run_2026_10": "Oct"}
ORIGINS = ["CN", "US", "EU"]
ORIGIN_NAME = {"CN": "China", "US": "United States", "EU": "European Union"}
SHORT = {
    "DeepSeek V4.1 Flash (MoE)": "DeepSeek V4.1 Flash",
    "Nemotron 3.5 Lightning (MoE)": "Nemotron 3.5 Lightning",
}


def short(name):
    return SHORT.get(name, name)


def unique_models():
    """One entry per model id, ordered by origin then first appearance (March first)."""
    seen = {}
    for m in MODELS:
        seen.setdefault(m["id"], {**m, "runs": []})["runs"].append(m["run"])
    out = []
    for o in ORIGINS:
        out.extend([m for m in seen.values() if m["origin"] == o])
    return out


# ---------------------------------------------------------------- f1: asymmetry by model
fig, ax = fs.new_fig()
fs.style_axes(ax)
ums = unique_models()
x = np.arange(len(ums), dtype=float)
# a small gap between origin groups
gap = 0
xs = []
prev = None
for i, m in enumerate(ums):
    if prev and m["origin"] != prev:
        gap += 0.9
    xs.append(i * 1.3 + gap)
    prev = m["origin"]
xs = np.array(xs)
w = 0.5
ax.axhline(0, color=fs.BASELINE, linewidth=1.2)
for i, m in enumerate(ums):
    both = len(m["runs"]) == 2
    for run in ("run_2026_03", "run_2026_10"):
        if run not in m["runs"]:
            continue
        a = RUNS[run]["metrics"]["bias_asymmetry"][m["id"]]["asymmetry"]
        off = (-w / 2 if run == "run_2026_03" else w / 2) if both else 0
        ax.bar(xs[i] + off, a, width=w, color=RUN_COLOR[run], zorder=3)
        lx, ha = xs[i] + off, "center"
        if both:  # nudge outward so the label clears the neighbouring bar
            lx, ha = (xs[i] + off + w / 2 - 0.02, "right") if run == "run_2026_03" else (xs[i] + off - w / 2 + 0.02, "left")
        ax.text(lx, a + (0.06 if a >= 0 else -0.06), f"{a:+.2f}", ha=ha,
                va="bottom" if a >= 0 else "top", fontsize=11 if both else 12, color=fs.INK2)
# Qwen3.8 27B without its empty responses
q = RUNS["run_2026_10"]["scores_with_without_empty"].get("qwen/qwen3.8-27b")
if q:
    i = [k for k, m in enumerate(ums) if m["id"] == "qwen/qwen3.8-27b"][0]
    v = q["without_empty"]["asymmetry"]["asymmetry"]
    ax.scatter([xs[i]], [v], marker="D", s=90, facecolors="white", edgecolors=fs.CAT[1], linewidths=2, zorder=4)
    ax.annotate(f"diamond: {v:+.2f} without\nits 9 empty responses", (xs[i], v), xytext=(xs[i] + 0.65, 2.05),
                textcoords="data", fontsize=11, color=fs.INK2, va="bottom", ha="center",
                arrowprops=dict(arrowstyle="-", color=fs.MUTED, lw=1, shrinkA=2, shrinkB=6))
ax.set_xticks(xs)
import textwrap  # noqa: E402
ax.set_xticklabels([textwrap.fill(short(m["name"]), 10) if len(short(m["name"])) > 10 else short(m["name"]).replace(" ", "\n", 1)
                    for m in ums], fontsize=12)
ax.set_ylabel("Asymmetry (other-region minus own-region score)")
ax.set_ylim(-1.05, 3.9)
# origin group labels
for o in ORIGINS:
    idx = [k for k, m in enumerate(ums) if m["origin"] == o]
    ax.text(xs[idx].mean(), 3.75, f"{ORIGIN_NAME[o]}-origin models", ha="center", va="top", fontsize=14,
            color=fs.INK, fontweight="bold")
ax.text(xs[-1] + 0.6, -0.95, "below zero: scores higher on its own region's topics", fontsize=12, color=fs.MUTED,
        ha="right", va="bottom")
ax.legend(handles=[Patch(color=RUN_COLOR[r], label=RUN_LABEL[r]) for r in RUN_COLOR],
          loc="upper right", bbox_to_anchor=(1.0, 0.9))
ax.set_title("Own-region asymmetry per model, March and October 2026", loc="left")
fs.finish(fig, os.path.join(OUT, "f1_asymmetry_by_model.png"))


# ---------------------------------------------------------------- f2: origin x topic heatmap
regions = ["CN", "US", "EU"]
rows, vals = [], []
for o in ORIGINS:
    for run in ("run_2026_03", "run_2026_10"):
        cells = RUNS[run]["origin_topic_matrix"]["cells"]
        rows.append((o, run))
        vals.append([cells[f"{o}_{r}"]["avg"] for r in regions])
vals = np.array(vals)
fig, ax = fs.new_fig()
cmap = fs.cmap_seq()
vmin, vmax = 5.0, 9.0
im = ax.imshow(vals, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
for i, (o, run) in enumerate(rows):
    for j, r in enumerate(regions):
        v = vals[i, j]
        col = cmap((v - vmin) / (vmax - vmin))
        hexcol = "#%02x%02x%02x" % tuple(int(c * 255) for c in col[:3])
        n = RUNS[run]["origin_topic_matrix"]["cells"][f"{o}_{r}"]["n_evals"]
        weight = "bold" if o == r else "normal"
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=17, color=fs.text_on(hexcol), fontweight=weight)
        ax.text(j, i + 0.3, f"n={n}", ha="center", va="center", fontsize=11, color=fs.text_on(hexcol))
        if o == r:
            ax.add_patch(__import__("matplotlib").patches.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                                                     edgecolor=fs.INK, linewidth=2.5))
ax.set_xticks(range(len(regions)))
ax.set_xticklabels([f"{ORIGIN_NAME[r]}-\nsensitive topics" for r in regions])
ax.xaxis.tick_top()
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([f"{o} models, {RUN_SHORT[run]}" for o, run in rows])
for k in (1.5, 3.5):
    ax.axhline(k, color=fs.SURFACE, linewidth=6)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
cb.set_label("Consensus score (0 to 10)")
cb.outline.set_visible(False)
ax.set_title("Score by subject origin and topic region (framed cells: own region)", loc="left", pad=70)
fs.finish(fig, os.path.join(OUT, "f2_origin_topic_heatmap.png"))


# ---------------------------------------------------------------- f3: refusal heatmap
cols = ["CN", "US", "EU", "neutral"]
rlabels, rvals, rtext = [], [], []
for m in unique_models():
    for run in ("run_2026_03", "run_2026_10"):
        if run not in m["runs"]:
            continue
        cr = RUNS[run]["refusal_classification_by_region"].get(m["id"], {})
        row, txt = [], []
        for c in cols:
            d = cr.get(c, {})
            tot = sum(d.values())
            non = tot - d.get("answered", 0)
            row.append(non / tot if tot else np.nan)
            kinds = [k for k in d if k != "answered"]
            # empty responses (no visible answer after long thinking) are labelled as such, not as refusals
            emp = [e for e in RUNS[run].get("empty_responses", {}).get(m["id"], [])
                   if e["category"] == "refusal_asymmetry" and (e["target_region"] or "untagged") == c]
            if emp and kinds == ["refused"] and len(emp) == non:
                kinds = ["no visible answer"]
            txt.append(f"{non}/{tot}" + (f"\n{', '.join(kinds)}" if kinds else ""))
        rlabels.append(f"{short(m['name'])} [{m['origin']}], {RUN_SHORT[run]}")
        rvals.append(row)
        rtext.append(txt)
rvals = np.array(rvals)
fig, ax = fs.new_fig(12, 8.5)
cmap = fs.cmap_seq()
im = ax.imshow(rvals, cmap=cmap, vmin=0, vmax=1, aspect="auto")
for i in range(rvals.shape[0]):
    for j in range(rvals.shape[1]):
        v = rvals[i, j]
        col = cmap(v)
        hexcol = "#%02x%02x%02x" % tuple(int(c * 255) for c in col[:3])
        ax.text(j, i, rtext[i][j].replace("\n", "  "), ha="center", va="center", fontsize=12, color=fs.text_on(hexcol))
ax.set_xticks(range(len(cols)))
ax.set_xticklabels(["China-sensitive", "US-sensitive", "EU-sensitive", "neutral control"])
ax.xaxis.tick_top()
ax.set_yticks(range(len(rlabels)))
ax.set_yticklabels(rlabels, fontsize=12)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.set_label("Share not answered (refused, hedged or deflected)")
cb.outline.set_visible(False)
ax.set_title("Refusal-asymmetry prompts not answered, by topic region (2 prompts per cell)", loc="left", pad=40)
fs.finish(fig, os.path.join(OUT, "f3_refusal_heatmap.png"))


# ---------------------------------------------------------------- f4: evaluator leniency
fig, ax = fs.new_fig()
fs.style_axes(ax)
evs = [("qwen/qwen3-235b-a22b-2507", "Qwen3 235B [CN]"), ("meta-llama/llama-3.3-70b-instruct", "Llama 3.3 70B [US]"),
       ("mistralai/mistral-large-2512", "Mistral Large 3 [EU]")]
pos = []
labels = []
k = 0
for eid, ename in evs:
    for run in ("run_2026_03", "run_2026_10"):
        ed = RUNS[run]["metrics"]["evaluator_disagreement"][eid]
        own, oth, len_ = ed["avg_score_own_origin_models"], ed["avg_score_other_origin_models"], ed["own_origin_leniency"]
        # dot plot (a truncated bar axis would exaggerate the gaps)
        ax.plot([k, k], [own, oth], color=fs.BASELINE, linewidth=2.5, zorder=2)
        ax.scatter([k], [own], s=170, color=fs.CAT[2], zorder=3)
        ax.scatter([k], [oth], s=170, color=fs.MUTED, zorder=3)
        hi_own = own >= oth
        ax.text(k + 0.13, own, f"{own:.2f}", ha="left", va="center", fontsize=12, color=fs.INK2)
        ax.text(k + 0.13, oth, f"{oth:.2f}", ha="left", va="center", fontsize=12, color=fs.INK2)
        ax.text(k, 9.5, f"{len_:+.2f}", ha="center", va="bottom", fontsize=15, fontweight="bold",
                color=fs.INK if abs(len_) >= 0.3 else fs.INK2)
        pos.append(k)
        labels.append(RUN_SHORT[run])
        k += 1
    k += 0.6
ax.set_xticks(pos)
ax.set_xticklabels(labels)
for i, (eid, ename) in enumerate(evs):
    ax.text((pos[2 * i] + pos[2 * i + 1]) / 2, 7.42, ename, ha="center", va="top", fontsize=14, color=fs.INK,
            fontweight="bold")
ax.set_ylim(7.6, 9.9)
ax.set_ylabel("Mean score this evaluator gave")
ax.text(pos[0] - 0.25, 9.72, "leniency (own minus other):", fontsize=12, color=fs.MUTED, ha="left", va="bottom")
ax.legend(handles=[Line2D([], [], marker="o", linestyle="", markersize=12, color=fs.CAT[2],
                          label="subjects from the evaluator's own origin"),
                   Line2D([], [], marker="o", linestyle="", markersize=12, color=fs.MUTED,
                          label="subjects from the other two origins")],
          loc="lower right")
ax.set_title("Does each judge favour models from its own origin?", loc="left", pad=28)
ax.tick_params(axis="x", pad=6)
fig.subplots_adjust(bottom=0.18)
fs.finish(fig, os.path.join(OUT, "f4_evaluator_leniency.png"))


# ---------------------------------------------------------------- f5: asymmetry vs release month
fig, ax = fs.new_fig()
fs.style_axes(ax, x_grid=False)
ax.axhline(0, color=fs.BASELINE, linewidth=1.2)
pts = []
for m in MODELS:
    d = dt.date(int(m["release"][:4]), int(m["release"][5:7]), 15)
    a = m["asymmetry"]
    col = RUN_COLOR[m["run"]]
    area = 40 + m["params_b"] * 18
    ax.scatter([d], [a], s=area, facecolors="none" if m["moe"] else col, edgecolors=col, linewidths=2.4,
               alpha=1 if m["moe"] else 0.75, zorder=4 if m["moe"] else 3)
    bridge = sum(1 for x in MODELS if x["id"] == m["id"]) > 1
    if m["id"] == "meta-llama/llama-3.1-8b-instruct":  # its label would run into Phi-4; put it above
        ax.annotate(f"{short(m['name'])} [{m['origin']}]", (d, a), xytext=(0, 22), textcoords="offset points",
                    fontsize=12, color=fs.INK2, ha="center", va="bottom")
        continue
    pts.append((mdates.date2num(d), a, f"{short(m['name'])} [{m['origin']}]" + (f", {RUN_SHORT[m['run']]}" if bridge else "")))
fs.place_labels(ax, pts, fontsize=12, min_gap=19, dx=24)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_xlim(dt.date(2024, 5, 1), dt.date(2027, 3, 1))
ax.set_ylim(-1.0, 3.8)
ax.set_ylabel("Own-region asymmetry")
ax.set_xlabel("Public release month of the model")
ax.legend(handles=[
    Line2D([], [], marker="o", linestyle="", markersize=11, markerfacecolor=RUN_COLOR["run_2026_03"],
           markeredgecolor=RUN_COLOR["run_2026_03"], label=RUN_LABEL["run_2026_03"]),
    Line2D([], [], marker="o", linestyle="", markersize=11, markerfacecolor=RUN_COLOR["run_2026_10"],
           markeredgecolor=RUN_COLOR["run_2026_10"], label=RUN_LABEL["run_2026_10"]),
    Line2D([], [], marker="o", linestyle="", markersize=11, markerfacecolor="white",
           markeredgecolor=fs.INK2, label="mixture-of-experts (area = active params)"),
], loc="upper left")
ax.set_title("Asymmetry by model generation (marker area grows with parameters)", loc="left")
fs.finish(fig, os.path.join(OUT, "f5_asymmetry_vs_release.png"))
