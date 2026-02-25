"""
Generate a professional 2D flowchart image for the
Structural Fatigue Simulation of a Bridge Beam.
Saves to: results/simulation_flowchart.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── Ensure results folder exists ──
os.makedirs("results", exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis("off")
fig.patch.set_facecolor("white")

# ── Title ──
ax.text(5, 19.4, "Simulation Flowchart", fontsize=18, fontweight="bold",
        ha="center", va="center", color="#2c3e50")
ax.text(5, 19.0, "Structural Fatigue in Bridge Beams Under Repeated Loading",
        fontsize=10, ha="center", va="center", color="#7f8c8d")

# ══════════════════════════════════════════════════════════════
#  Helper functions
# ══════════════════════════════════════════════════════════════

def draw_box(ax, cx, cy, w, h, text, color="#3498db", text_color="white",
             fontsize=9, shape="rect", subtext=None):
    """Draw a flowchart box (rectangle or diamond)."""
    if shape == "diamond":
        # Diamond for decision
        diamond = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor="#2c3e50", linewidth=1.5,
            transform=ax.transData, zorder=3
        )
        ax.add_patch(diamond)
        ax.text(cx, cy + 0.08, text, fontsize=fontsize, fontweight="bold",
                ha="center", va="center", color=text_color, zorder=4)
        if subtext:
            ax.text(cx, cy - 0.22, subtext, fontsize=7, ha="center",
                    va="center", color=text_color, style="italic", zorder=4)
    elif shape == "stadium":
        # Rounded pill for start/end
        box = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.15",
            facecolor=color, edgecolor="#2c3e50", linewidth=2,
            zorder=3
        )
        ax.add_patch(box)
        ax.text(cx, cy, text, fontsize=fontsize, fontweight="bold",
                ha="center", va="center", color=text_color, zorder=4)
    else:
        box = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.1",
            facecolor=color, edgecolor="#2c3e50", linewidth=1.5,
            zorder=3
        )
        ax.add_patch(box)
        # Main text
        if subtext:
            ax.text(cx, cy + 0.15, text, fontsize=fontsize, fontweight="bold",
                    ha="center", va="center", color=text_color, zorder=4)
            ax.text(cx, cy - 0.15, subtext, fontsize=7, ha="center",
                    va="center", color=text_color, zorder=4)
        else:
            ax.text(cx, cy, text, fontsize=fontsize, fontweight="bold",
                    ha="center", va="center", color=text_color, zorder=4)


def arrow(ax, x1, y1, x2, y2, label=None, label_side="right"):
    """Draw an arrow between two points with optional label."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#2c3e50",
                                lw=1.8, mutation_scale=15),
                zorder=2)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        offset = 0.25 if label_side == "right" else -0.25
        ax.text(mx + offset, my, label, fontsize=8, fontweight="bold",
                ha="center", va="center", color="#2c3e50",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ecf0f1",
                          edgecolor="#bdc3c7", linewidth=0.8),
                zorder=5)


# ══════════════════════════════════════════════════════════════
#  Layout coordinates  (cx, cy)
# ══════════════════════════════════════════════════════════════

cx = 5.0   # center column
bw = 4.0   # box width
bh = 0.65  # box height

y_start    = 18.0
y_params   = 16.8
y_init     = 15.6
y_process  = 14.2
y_decide   = 12.7
y_dispose  = 11.2
y_anim     = 9.5
y_3d       = 8.3
y_save     = 7.1
y_console  = 5.9
y_end      = 4.7

# ── CADPD labels on the left side ──
cadpd_x = 0.55
cadpd_data = [
    (y_params + 0.35, "CREATE", "#27ae60"),
    (y_init,          "ASSIGN", "#2980b9"),
    (y_process,       "PROCESS", "#8e44ad"),
    (y_decide,        "DECIDE", "#e67e22"),
    (y_dispose,       "DISPOSE", "#c0392b"),
]
for (yy, label, col) in cadpd_data:
    ax.text(cadpd_x, yy, label, fontsize=7, fontweight="bold",
            ha="center", va="center", rotation=0, color="white",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=col,
                      edgecolor=col, linewidth=0),
            zorder=5)

# ══════════════════════════════════════════════════════════════
#  Draw boxes
# ══════════════════════════════════════════════════════════════

#  START
draw_box(ax, cx, y_start, 2.5, 0.6, "START", color="#2ecc71",
         text_color="white", fontsize=12, shape="stadium")

#  Set Parameters
draw_box(ax, cx, y_params, bw, bh, "Set Parameters",
         color="#27ae60", subtext="damage_increment, failure_threshold, segment_factors")

#  Initialize Segments
draw_box(ax, cx, y_init, bw, bh, "Initialize 3 Beam Segments",
         color="#2980b9", subtext="damage = 0.0 for each segment")

#  Loop bracket background
loop_rect = mpatches.FancyBboxPatch(
    (cx - bw / 2 - 0.35, y_dispose - 0.55), bw + 0.7, y_process - y_dispose + 1.3,
    boxstyle="round,pad=0.15", facecolor="#f0f4f8", edgecolor="#95a5a6",
    linewidth=1.2, linestyle="--", zorder=1)
ax.add_patch(loop_rect)
ax.text(cx, y_process + 0.65, "CYCLE LOOP  (repeat until failure)",
        fontsize=8, fontweight="bold", ha="center", va="center",
        color="#7f8c8d", style="italic", zorder=2)

#  Process damage
draw_box(ax, cx, y_process, bw, bh, "Accumulate Damage",
         color="#8e44ad", subtext="damage[i] += damage_increment * segment_factor[i]")

#  Decision
draw_box(ax, cx, y_decide, bw, 0.75, "damage >= threshold?",
         color="#e67e22", text_color="white", fontsize=10, shape="rect",
         subtext="Check each segment for failure")

#  Dispose / Failure
draw_box(ax, cx, y_dispose, bw, bh, "FAILURE DETECTED",
         color="#c0392b", subtext="Mark segment as FAILED  --  Stop simulation")

#  Display 2D
draw_box(ax, cx, y_anim, bw, bh, "Display Animated 2D Visualization",
         color="#2c3e50", subtext="Color-coded beam, damage gauge, live chart")

#  Display 3D
draw_box(ax, cx, y_3d, bw, bh, "Display 3D Beam Model",
         color="#2c3e50", subtext="Final-state beam with crack effects")

#  Save results
draw_box(ax, cx, y_save, bw, bh, "Save Result Charts (PNG)",
         color="#2c3e50", subtext="damage_distribution.png, damage_over_time.png")

#  Console summary
draw_box(ax, cx, y_console, bw, bh, "Print Console Summary",
         color="#2c3e50", subtext="Cycle of failure, max damage, beam status")

#  END
draw_box(ax, cx, y_end, 2.5, 0.6, "END", color="#e74c3c",
         text_color="white", fontsize=12, shape="stadium")


# ══════════════════════════════════════════════════════════════
#  Draw arrows
# ══════════════════════════════════════════════════════════════

# START → Set Parameters
arrow(ax, cx, y_start - 0.30, cx, y_params + 0.35)

# Set Parameters → Initialize
arrow(ax, cx, y_params - 0.35, cx, y_init + 0.35)

# Initialize → Process (into loop)
arrow(ax, cx, y_init - 0.35, cx, y_process + 0.35)

# Process → Decide
arrow(ax, cx, y_process - 0.35, cx, y_decide + 0.40)

# Decide → YES → Dispose (Failure)
arrow(ax, cx, y_decide - 0.40, cx, y_dispose + 0.35, label="YES")

# Decide → NO → loop back  (right side arc)
loop_x = cx + bw / 2 + 0.6
ax.annotate("", xy=(loop_x, y_process), xytext=(loop_x, y_decide),
            arrowprops=dict(arrowstyle="-", color="#27ae60", lw=2,
                            connectionstyle="arc3,rad=0"),
            zorder=2)
ax.annotate("", xy=(cx + bw / 2 + 0.02, y_process),
            xytext=(loop_x, y_process),
            arrowprops=dict(arrowstyle="-|>", color="#27ae60", lw=2,
                            mutation_scale=14),
            zorder=2)
# horizontal stub from decide box
ax.plot([cx + bw / 2 + 0.02, loop_x], [y_decide, y_decide],
        color="#27ae60", lw=2, zorder=2)
ax.text(loop_x + 0.35, (y_decide + y_process) / 2, "NO\n(next\ncycle)",
        fontsize=7, fontweight="bold", ha="center", va="center",
        color="#27ae60", zorder=5)

# Dispose → Display 2D
arrow(ax, cx, y_dispose - 0.35, cx, y_anim + 0.35)

# 2D → 3D
arrow(ax, cx, y_anim - 0.35, cx, y_3d + 0.35)

# 3D → Save
arrow(ax, cx, y_3d - 0.35, cx, y_save + 0.35)

# Save → Console
arrow(ax, cx, y_save - 0.35, cx, y_console + 0.35)

# Console → END
arrow(ax, cx, y_console - 0.35, cx, y_end + 0.30)


# ══════════════════════════════════════════════════════════════
#  Footer
# ══════════════════════════════════════════════════════════════

ax.text(5, 4.05, "A Python-Based Simulation of Structural Fatigue in Bridge Beams",
        fontsize=7, ha="center", va="center", color="#95a5a6")
ax.text(5, 3.75, "Modeling & Simulation  |  Conceptual / Normalized Model",
        fontsize=7, ha="center", va="center", color="#95a5a6")

# ── Save ──
plt.tight_layout()
out_path = os.path.join("results", "simulation_flowchart.png")
fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Flowchart saved to: {out_path}")
