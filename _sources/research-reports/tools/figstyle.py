"""Shared matplotlib style for the research-report figures (projector-first).

Palette = the validated reference instance of the dataviz method (light surface):
categorical slots in fixed order (never cycled), one-hue sequential ramp, blue/red
diverging pair with a neutral grey midpoint, reserved status colours. Figures are
PNGs on a light surface; the Riso reader puts them on a light card in Night mode.

Usage in a report's figures/build_figures.py:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
    import figstyle as fs
    fs.apply()
    fig, ax = fs.new_fig()
    ...
    fs.finish(fig, "/abs/path/to/slug/figures/f1_name.png")
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- colour roles (light surface) -------------------------------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
DEEMPH = "#c3c2b7"          # "the rest" in an emphasis chart

# categorical, fixed order: blue, orange, aqua, yellow, magenta, green, violet, red
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
# the first three validate all-pairs (scatter, small multiples): use for CN / US / EU etc.
CAT3 = CAT[:3]

# sequential blue ramp, light -> dark (steps 100..700)
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
       "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
# diverging: blue pole, neutral grey midpoint, red pole
DIV = ["#0d366b", "#2a78d6", "#86b6ef", "#f0efec", "#f3a9a8", "#e34948", "#8f1d1d"]

STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}

FONT = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]


def apply(base=16):
    """Projector-sized type: base 16pt on a 12x7in canvas at 160 dpi."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": FONT,
        "font.size": base,
        "axes.titlesize": base + 4,
        "axes.titleweight": "bold",
        "axes.labelsize": base,
        "xtick.labelsize": base - 2,
        "ytick.labelsize": base - 2,
        "legend.fontsize": base - 2,
        "figure.titlesize": base + 6,
        "axes.edgecolor": BASELINE,
        "axes.labelcolor": INK2,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "lines.linewidth": 2,
        "lines.markersize": 9,
        "legend.frameon": False,
        "figure.dpi": 100,
        "savefig.dpi": 160,
    })


def new_fig(w=12, h=7, **kw):
    fig, ax = plt.subplots(figsize=(w, h), **kw)
    return fig, ax


def style_axes(ax, y_grid=True, x_grid=False):
    """Recessive chrome: hairline grid behind the marks, muted ticks, baseline only."""
    ax.set_axisbelow(True)
    if y_grid:
        ax.yaxis.grid(True, color=GRID, linewidth=1)
    if x_grid:
        ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.tick_params(length=0)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
        ax.spines[side].set_linewidth(1)


def cmap_seq():
    return LinearSegmentedColormap.from_list("seq_blue", SEQ)


def cmap_div():
    return LinearSegmentedColormap.from_list("div_blue_red", DIV)


def text_on(hexcolor):
    """Ink colour that stays legible on a filled cell (light ink on dark fills)."""
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#f0efec" if lum < 0.5 else INK


def finish(fig, path, pad=0.4):
    fig.tight_layout(pad=pad)
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", path)


def place_labels(ax, pts, fontsize=10.5, min_gap=15, x_group=None, color=None, dx=8, iters=300):
    """Direct labels without collisions: pts = [(x, y, text), ...] in data coords.

    Every label starts beside its point; labels whose text boxes overlap horizontally are pushed
    apart vertically (simple pairwise repulsion in display pixels) until no pair is closer than
    `min_gap`, then the whole set is kept inside the axes. A label moved more than 6 px from its
    point gets a thin leader line. `x_group` is accepted for backward compatibility and ignored.
    """
    fig = ax.get_figure()
    fig.canvas.draw()
    disp = ax.transData.transform([(x, y) for x, y, _ in pts])
    char_w = fontsize * fig.dpi / 72 * 0.55          # rough average glyph width in px
    boxes = []
    for (x, y, text), (px, py) in zip(pts, disp):
        boxes.append([px + dx, px + dx + char_w * len(text), py])   # x0, x1, y (mutable)
    top = ax.bbox.y1 - 8
    bottom = ax.bbox.y0 + 8
    for _ in range(iters):
        moved = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[1] and b[0] < a[1]:                  # horizontal overlap
                    dy = b[2] - a[2]
                    if abs(dy) < min_gap:
                        push = (min_gap - abs(dy)) / 2 + 0.5
                        if dy >= 0:
                            a[2] -= push
                            b[2] += push
                        else:
                            a[2] += push
                            b[2] -= push
                        moved = True
        for bx in boxes:
            bx[2] = min(max(bx[2], bottom), top)
        if not moved:
            break
    inv = ax.transData.inverted()
    for (x, y, text), (px, py), bx in zip(pts, disp, boxes):
        lx, ly = inv.transform((bx[0], bx[2]))
        moved = abs(bx[2] - py) > 6
        ax.annotate(text, (x, y), xytext=(lx, ly), textcoords="data", fontsize=fontsize,
                    color=color or INK2, va="center", ha="left",
                    arrowprops=dict(arrowstyle="-", color=GRID, lw=1, shrinkA=0, shrinkB=4) if moved else None)
