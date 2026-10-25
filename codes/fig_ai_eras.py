# 서론 그림 — ChatGPT 의 등장(1.0) → Claude Code 의 등장(2.0? 1.5?) — 글 대신 그림으로 (대표 10-26 «그림으로 그려야지»)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Polygon, Rectangle

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}\usepackage{kotex}"
BLUE, ORANGE, GRAY, INK = "#2b6cb0", "#c05621", "#718096", "#2d3748"

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.set_xlim(0, 16); ax.set_ylim(0, 7.6); ax.set_aspect("equal"); ax.axis("off")

def person(x, y, c=INK, s=1.0):
    ax.add_patch(Circle((x, y + 0.75 * s), 0.32 * s, fc=c, ec="none"))
    ax.add_patch(FancyBboxPatch((x - 0.48 * s, y - 0.25 * s), 0.96 * s, 0.75 * s,
                                boxstyle="round,pad=0,rounding_size=0.35", fc=c, ec="none"))
def robot(x, y, c=ORANGE):
    ax.add_patch(FancyBboxPatch((x - 0.6, y - 0.45), 1.2, 0.95, boxstyle="round,pad=0,rounding_size=0.25", fc=c, ec="none"))
    for dx in (-0.25, 0.25): ax.add_patch(Circle((x + dx, y + 0.05), 0.11, fc="white", ec="none"))
    ax.plot([x, x], [y + 0.5, y + 0.8], color=c, lw=2); ax.add_patch(Circle((x, y + 0.85), 0.09, fc=c, ec="none"))
def doc(x, y, c=GRAY):
    ax.add_patch(Polygon([(x - 0.4, y - 0.55), (x + 0.4, y - 0.55), (x + 0.4, y + 0.3), (x + 0.15, y + 0.55), (x - 0.4, y + 0.55)], fc="white", ec=c, lw=1.4))
    for k in range(3): ax.plot([x - 0.25, x + 0.25], [y + 0.15 - k * 0.22] * 2, color=c, lw=1.2)
def terminal(x, y):
    ax.add_patch(FancyBboxPatch((x - 0.55, y - 0.42), 1.1, 0.84, boxstyle="round,pad=0,rounding_size=0.08", fc="#1a202c", ec="none"))
    ax.text(x - 0.38, y - 0.05, r"\texttt{>\_}", color="#68d391", fontsize=9, va="center")
def folder(x, y, c="#d69e2e"):
    ax.add_patch(Polygon([(x - 0.55, y - 0.4), (x + 0.55, y - 0.4), (x + 0.55, y + 0.3), (x - 0.05, y + 0.3), (x - 0.2, y + 0.45), (x - 0.55, y + 0.45)], fc=c, ec="none"))
def globe(x, y, c=BLUE):
    ax.add_patch(Circle((x, y), 0.45, fc="white", ec=c, lw=1.4))
    ax.add_patch(Ellipse((x, y), 0.4, 0.9, fc="none", ec=c, lw=1.0)); ax.plot([x - 0.45, x + 0.45], [y, y], color=c, lw=1.0)
def bubble(x, y, w, c, right=False):
    ax.add_patch(FancyBboxPatch((x, y), w, 0.42, boxstyle="round,pad=0,rounding_size=0.18", fc=c, ec="none"))
def arrow(a, b, c=INK, lw=1.5, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=13, lw=lw, color=c, linestyle=ls))

# ── 1.0 ChatGPT ───────────────────────────────
ax.text(3.6, 7.05, r"\textbf{1.0} \; ChatGPT", ha="center", fontsize=15, color=BLUE)
ax.text(3.6, 6.5, r"2022년 11월", ha="center", fontsize=9, color=GRAY)
person(0.9, 3.6)
ax.add_patch(FancyBboxPatch((2.0, 2.4), 3.2, 3.4, boxstyle="round,pad=0,rounding_size=0.25", fc="#ebf4ff", ec=BLUE, lw=1.4))
bubble(3.4, 4.95, 1.55, "#bee3f8"); bubble(2.25, 4.3, 2.4, "white"); bubble(3.6, 3.65, 1.35, "#bee3f8"); bubble(2.25, 3.0, 2.0, "white")
ax.text(3.6, 2.0, r"묻고 답하기", ha="center", fontsize=10, color=INK)
arrow((1.45, 3.9), (2.0, 4.2), c=INK)
doc(6.4, 3.9); arrow((5.25, 3.9), (5.9, 3.9), c=GRAY, ls="--")
ax.text(6.4, 2.95, r"사람이 옮겨 붙임", ha="center", fontsize=8.5, color=GRAY)

# ── 가운데 화살표 ─────────────────────────────
arrow((7.35, 3.9), (8.65, 3.9), c=INK, lw=2.2)
ax.text(8.0, 4.45, r"1.5? \; 2.0?", ha="center", fontsize=10.5, color=INK)

# ── 2.0? Claude Code ─────────────────────────
ax.text(12.4, 7.05, r"\textbf{2.0?} \; Claude Code", ha="center", fontsize=15, color=ORANGE)
ax.text(12.4, 6.5, r"2025년", ha="center", fontsize=9, color=GRAY)
person(9.4, 3.6)
robot(11.6, 3.9)
arrow((9.95, 4.15), (10.9, 4.15), c=INK); ax.text(10.45, 4.5, r"맡김", ha="center", fontsize=8.5, color=INK)
arrow((10.9, 3.55), (9.95, 3.55), c=GRAY, ls="--"); ax.text(10.45, 3.0, r"확인", ha="center", fontsize=8.5, color=GRAY)
tools = [(14.6, 5.6, folder, r"파일"), (14.6, 4.3, terminal, r"터미널"), (14.6, 3.0, globe, r"웹"), (14.6, 1.7, doc, r"문서")]
for tx, ty, f, lab in tools:
    f(tx, ty); ax.text(tx + 0.85, ty, lab, ha="left", va="center", fontsize=8.5, color=INK)
    arrow((12.25, 3.9), (tx - 0.65, ty), c=ORANGE, lw=1.3)
ax.text(11.6, 2.75, r"직접 열고 고치고 실행", ha="center", fontsize=9.5, color=INK)

fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(f"figs/ai_eras.{ext}", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved")
