"""
============================================================
  STRUCTURAL FATIGUE SIMULATION OF A BRIDGE BEAM
  Conceptual / Normalized Model
============================================================

HOW TO USE:
  1. Change the parameters below to manipulate the simulation
  2. Run: python simulation.py
  3. Watch the animated 2D visualization
  4. Close the window → 3D beam view appears
  5. Close that → summary results are saved as images

SIMULATION LOGIC:
  Each cycle = one repeated load application
  damage += damage_increment * segment_factor
  If damage >= failure_threshold → FAILURE

============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# ================================================================
#   MANIPULABLE PARAMETERS — CHANGE THESE TO CONTROL THE SIMULATION
# ================================================================

damage_increment = 0.002      # Damage added per cycle (normalized, 0 to 1)
failure_threshold = 1.0       # When damage reaches this value → FAILURE
num_segments = 3              # Number of beam segments (matches conceptual model)
animation_speed = 20          # Milliseconds between frames (lower = faster)
cycles_per_frame = 2          # How many cycles to advance per animation frame

# Segment damage multipliers (center segment gets more damage)
# Segment 1 (left): 0.5x, Segment 2 (center): 1.0x, Segment 3 (right): 0.5x
segment_factors = [0.5, 1.0, 0.5]

# ================================================================
#   END OF PARAMETERS — Code below runs the simulation
# ================================================================


def get_damage_color(damage, threshold):
    """Return color based on damage level."""
    ratio = damage / threshold
    if ratio < 0.25:
        return '#2ecc71'   # Green — SAFE
    elif ratio < 0.50:
        return '#f1c40f'   # Yellow — LOW
    elif ratio < 0.75:
        return '#e67e22'   # Orange — WARNING
    else:
        return '#e74c3c'   # Red — CRITICAL / FAILED


def get_status_text(damage, threshold):
    """Return status label based on damage level."""
    ratio = damage / threshold
    if ratio < 0.25:
        return 'SAFE', '#2ecc71'
    elif ratio < 0.50:
        return 'LOW DAMAGE', '#f1c40f'
    elif ratio < 0.75:
        return 'WARNING', '#e67e22'
    elif ratio < 1.0:
        return 'CRITICAL', '#e74c3c'
    else:
        return 'FAILED', '#c0392b'


def get_beam_status(damages, threshold):
    """Return overall beam status."""
    max_d = max(damages)
    if max_d >= threshold:
        return 'FAILED', '#e74c3c'
    elif max_d >= threshold * 0.75:
        return 'WARNING', '#e67e22'
    elif max_d >= threshold * 0.25:
        return 'SAFE', '#2ecc71'
    else:
        return 'SAFE', '#2ecc71'


# ================================================================
#   RUN SIMULATION (collect all data first)
# ================================================================

print("=" * 55)
print("  STRUCTURAL FATIGUE SIMULATION OF A BRIDGE BEAM")
print("  Conceptual / Normalized Model")
print("=" * 55)
print(f"\n  Parameters:")
print(f"    Damage Increment:  {damage_increment}")
print(f"    Failure Threshold: {failure_threshold}")
print(f"    Segments:          {num_segments}")
print(f"    Segment Factors:   {segment_factors}")
print(f"    Mode:              Run until failure")
print()

# Initialize
beam_segments = [0.0] * num_segments
history_cycles = []
history_damages = [[] for _ in range(num_segments)]
history_max_damage = []
failure_cycle = None

# Simulation loop — runs until failure (a segment reaches the threshold)
cycle = 0
while True:
    cycle += 1
    for i in range(num_segments):
        beam_segments[i] += damage_increment * segment_factors[i]

    # Record history
    history_cycles.append(cycle)
    for i in range(num_segments):
        history_damages[i].append(beam_segments[i])
    history_max_damage.append(max(beam_segments))

    # Console output every 50 cycles
    if cycle % 50 == 0 or cycle == 1:
        seg_str = " | ".join([f"S{i+1}: {beam_segments[i]:.3f}" for i in range(num_segments)])
        print(f"  Cycle {cycle:>4}: {seg_str}")

    # Check failure
    for i in range(num_segments):
        if beam_segments[i] >= failure_threshold:
            if failure_cycle is None:
                failure_cycle = cycle
                print(f"\n  [!] FAILURE! Segment {i+1} failed at cycle {cycle}")
                print(f"    Damage = {beam_segments[i]:.3f} >= {failure_threshold}")

    if failure_cycle is not None:
        break

print()

# ================================================================
#   ANIMATED 2D VISUALIZATION
# ================================================================

print("  Opening animated 2D visualization...")

fig = plt.figure(figsize=(14, 9))
fig.patch.set_facecolor('#fafafa')
gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Title
fig.suptitle("Structural Fatigue Simulation of a Bridge Beam",
             fontsize=16, fontweight='bold', y=0.97, color='#2c3e50')

# --- Top row: Beam visualization ---
ax_beam = fig.add_subplot(gs[0, :])
ax_beam.set_xlim(-0.5, num_segments + 0.5)
ax_beam.set_ylim(-0.8, 1.8)
ax_beam.set_aspect('equal')
ax_beam.axis('off')

# Static beam elements
ax_beam.set_title("Bridge Beam", fontsize=12, fontweight='bold', color='#2c3e50')

# Load arrow (static)
mid = num_segments / 2
ax_beam.annotate('', xy=(mid, 1.0), xytext=(mid, 1.6),
                 arrowprops=dict(arrowstyle='->', color='red', lw=3))
ax_beam.text(mid, 1.7, 'Repeated Load', ha='center', fontsize=10,
             fontweight='bold', color='red')

# Supports (triangles)
support_size = 0.15
ax_beam.plot([0, -support_size, support_size, 0],
             [-0.1, -0.35, -0.35, -0.1], 'k-', lw=2)
ax_beam.plot([num_segments, num_segments - support_size, num_segments + support_size, num_segments],
             [-0.1, -0.35, -0.35, -0.1], 'k-', lw=2)

# Segment rectangles (will be updated)
seg_patches = []
seg_texts = []
seg_label_texts = []
for i in range(num_segments):
    rect = mpatches.FancyBboxPatch((i + 0.05, 0.0), 0.9, 0.8,
                                    boxstyle="round,pad=0.02",
                                    facecolor='#2ecc71', edgecolor='#2c3e50',
                                    linewidth=2)
    ax_beam.add_patch(rect)
    seg_patches.append(rect)

    txt = ax_beam.text(i + 0.5, 0.4, "0.0%", ha='center', va='center',
                       fontsize=11, fontweight='bold', color='white')
    seg_texts.append(txt)

    lbl = ax_beam.text(i + 0.5, -0.15, f"Segment {i+1}", ha='center',
                       fontsize=8, color='#7f8c8d')
    seg_label_texts.append(lbl)

# --- Middle left: Damage gauge ---
ax_gauge = fig.add_subplot(gs[1, 0])
ax_gauge.set_title("Fatigue Damage Indicator", fontsize=10, fontweight='bold', color='#2c3e50')
ax_gauge.set_xlim(0, 1)
ax_gauge.set_ylim(0, 1.15)
ax_gauge.set_xticks([])
ax_gauge.set_yticks([])

# Gauge background
gauge_bg = mpatches.FancyBboxPatch((0.15, 0.05), 0.7, 0.85,
                                    boxstyle="round,pad=0.03",
                                    facecolor='#ecf0f1', edgecolor='#bdc3c7', lw=2)
ax_gauge.add_patch(gauge_bg)

# Gauge fill bar (will be updated)
gauge_fill = mpatches.Rectangle((0.25, 0.1), 0.5, 0.0,
                                 facecolor='#2ecc71', edgecolor='none')
ax_gauge.add_patch(gauge_fill)

# Gauge border
gauge_border = mpatches.Rectangle((0.25, 0.1), 0.5, 0.7,
                                   facecolor='none', edgecolor='#2c3e50', lw=2)
ax_gauge.add_patch(gauge_border)

# Threshold line
ax_gauge.plot([0.22, 0.78], [0.1 + 0.7, 0.1 + 0.7], 'r--', lw=2)
ax_gauge.text(0.5, 0.83, 'FAILURE', ha='center', fontsize=7, color='red', fontweight='bold')

gauge_pct_text = ax_gauge.text(0.5, 0.95, "0%", ha='center', fontsize=18, fontweight='bold', color='#2c3e50')

# --- Middle center: Beam Status ---
ax_status = fig.add_subplot(gs[1, 1])
ax_status.set_xlim(0, 1)
ax_status.set_ylim(0, 1)
ax_status.set_xticks([])
ax_status.set_yticks([])
ax_status.set_title("Beam Status", fontsize=10, fontweight='bold', color='#2c3e50')

status_bg = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                                     boxstyle="round,pad=0.05",
                                     facecolor='#2ecc71', edgecolor='#2c3e50', lw=2)
ax_status.add_patch(status_bg)
status_text = ax_status.text(0.5, 0.55, "SAFE", ha='center', va='center',
                              fontsize=22, fontweight='bold', color='white')
status_bullet_1 = ax_status.text(0.15, 0.3, "● SAFE", fontsize=8, color='white')
status_bullet_2 = ax_status.text(0.15, 0.2, "● WARNING", fontsize=8, color='white')
status_bullet_3 = ax_status.text(0.55, 0.3, "● CRITICAL", fontsize=8, color='white')
status_bullet_4 = ax_status.text(0.55, 0.2, "● FAILED", fontsize=8, color='white')

# --- Middle right: Cycle counter ---
ax_info = fig.add_subplot(gs[1, 2])
ax_info.set_xlim(0, 1)
ax_info.set_ylim(0, 1)
ax_info.set_xticks([])
ax_info.set_yticks([])
ax_info.set_title("Simulation Info", fontsize=10, fontweight='bold', color='#2c3e50')

info_bg = mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                   boxstyle="round,pad=0.05",
                                   facecolor='#ecf0f1', edgecolor='#bdc3c7', lw=2)
ax_info.add_patch(info_bg)

cycle_text = ax_info.text(0.5, 0.78, "Cycle: 0", ha='center', fontsize=14, fontweight='bold', color='#2c3e50')
param_texts = [
    ax_info.text(0.12, 0.58, f"Damage/Cycle: {damage_increment}", fontsize=8, color='#7f8c8d'),
    ax_info.text(0.12, 0.46, f"Threshold: {failure_threshold}", fontsize=8, color='#7f8c8d'),
    ax_info.text(0.12, 0.34, f"Segments: {num_segments}", fontsize=8, color='#7f8c8d'),
    ax_info.text(0.12, 0.22, f"Factors: {segment_factors}", fontsize=8, color='#7f8c8d'),
    ax_info.text(0.12, 0.10, f"Mode: Run until failure", fontsize=8, color='#7f8c8d'),
]

# --- Bottom row: Damage over time chart ---
ax_chart = fig.add_subplot(gs[2, :])
ax_chart.set_title("Fatigue Damage Over Load Cycles", fontsize=10, fontweight='bold', color='#2c3e50')
ax_chart.set_xlabel("Load Cycles", fontsize=9)
ax_chart.set_ylabel("Damage", fontsize=9)
ax_chart.set_xlim(0, len(history_cycles))
ax_chart.set_ylim(0, max(failure_threshold * 1.15, 1.15))
ax_chart.axhline(y=failure_threshold, color='red', linewidth=1.5, linestyle='--', alpha=0.7, label='Failure Threshold')
ax_chart.grid(True, alpha=0.2)

seg_colors_line = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#e67e22']
lines = []
for i in range(num_segments):
    line, = ax_chart.plot([], [], '-', linewidth=2,
                          color=seg_colors_line[i % len(seg_colors_line)],
                          label=f'Segment {i+1}')
    lines.append(line)
ax_chart.legend(loc='upper left', fontsize=8)


# Animation update function
total_frames = len(history_cycles)

def animate(frame_idx):
    idx = min(frame_idx * cycles_per_frame, total_frames - 1)

    # Update beam segment colors and text
    for i in range(num_segments):
        d = history_damages[i][idx]
        color = get_damage_color(d, failure_threshold)
        seg_patches[i].set_facecolor(color)
        pct = min(d / failure_threshold * 100, 100)
        seg_texts[i].set_text(f"{pct:.0f}%")

    # Update gauge
    max_d = history_max_damage[idx]
    fill_height = min(max_d / failure_threshold, 1.0) * 0.7
    gauge_fill.set_height(fill_height)
    gauge_fill.set_facecolor(get_damage_color(max_d, failure_threshold))
    pct = min(max_d / failure_threshold * 100, 100)
    gauge_pct_text.set_text(f"{pct:.0f}%")

    # Update status
    status_label, status_color = get_beam_status(
        [history_damages[i][idx] for i in range(num_segments)], failure_threshold)
    status_bg.set_facecolor(status_color)
    status_text.set_text(status_label)

    # Update cycle counter
    cycle_text.set_text(f"Cycle: {history_cycles[idx]}")

    # Update chart lines
    for i in range(num_segments):
        lines[i].set_data(history_cycles[:idx+1], history_damages[i][:idx+1])

    return seg_patches + seg_texts + [gauge_fill, gauge_pct_text, status_bg, status_text, cycle_text] + lines


num_frames = (total_frames + cycles_per_frame - 1) // cycles_per_frame

anim = animation.FuncAnimation(fig, animate, frames=num_frames,
                                interval=animation_speed, blit=False, repeat=False)

try:
    fig.tight_layout(rect=[0, 0, 1, 0.95])
except Exception:
    pass  # tight_layout may warn with mixed axes
plt.show()


# ================================================================
#   3D BEAM VISUALIZATION (after closing animation)
# ================================================================

print("  Opening 3D beam visualization...")

fig3d = plt.figure(figsize=(12, 7))
ax3d = fig3d.add_subplot(111, projection='3d')

beam_length = 10.0
seg_length = beam_length / num_segments
width = 1.5
height = 1.0

# Use final damage values
final_damages = [history_damages[i][-1] for i in range(num_segments)]

for i in range(num_segments):
    x0 = i * seg_length
    x1 = x0 + seg_length
    y0, y1 = -width / 2, width / 2
    z0, z1 = 0, height

    color = get_damage_color(final_damages[i], failure_threshold)

    faces = [
        [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]],  # bottom
        [[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]],  # top
        [[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1]],  # front
        [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],  # back
        [[x0, y0, z0], [x0, y1, z0], [x0, y1, z1], [x0, y0, z1]],  # left
        [[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]],  # right
    ]

    poly = Poly3DCollection(faces, alpha=0.85)
    poly.set_facecolor(color)
    poly.set_edgecolor('#2c3e50')
    poly.set_linewidth(0.8)
    ax3d.add_collection3d(poly)

    # Damage label on top
    pct = min(final_damages[i] / failure_threshold * 100, 100)
    ax3d.text((x0 + x1) / 2, 0, height + 0.3, f"S{i+1}\n{pct:.0f}%",
              ha='center', va='bottom', fontsize=10, fontweight='bold',
              color='#2c3e50')

    # Crack lines for damaged segments
    if final_damages[i] >= failure_threshold * 0.5:
        mid_x = (x0 + x1) / 2
        crack_intensity = min(final_damages[i] / failure_threshold, 1.0)
        for j in range(int(crack_intensity * 5) + 1):
            cx = mid_x + np.random.uniform(-seg_length * 0.3, seg_length * 0.3)
            cy = np.random.uniform(-width * 0.3, width * 0.3)
            ax3d.plot([cx, cx], [cy, cy], [z0, z0 + height * crack_intensity * 0.8],
                      'k-', linewidth=1.5, alpha=0.7)

# Supports
ax3d.scatter([0], [0], [0], color='green', s=200, marker='^', label='Support A', zorder=5)
ax3d.scatter([beam_length], [0], [0], color='orange', s=200, marker='o', label='Support B', zorder=5)

# Load arrow
mid_x = beam_length / 2
ax3d.quiver(mid_x, 0, height + 1.5, 0, 0, -1.0,
            color='red', arrow_length_ratio=0.3, linewidth=3)
ax3d.text(mid_x, 0, height + 2.0, 'LOAD', color='red',
          fontsize=12, ha='center', fontweight='bold')

ax3d.set_xlabel('Beam Length (m)')
ax3d.set_ylabel('Width (m)')
ax3d.set_zlabel('Height (m)')

total_cycles_run = history_cycles[-1]
status_label, _ = get_beam_status(final_damages, failure_threshold)
ax3d.set_title(f"3D Bridge Beam — Final State After {total_cycles_run} Cycles\n"
               f"Status: {status_label} | Max Damage: {max(final_damages):.1%}",
               fontsize=13, fontweight='bold')
ax3d.legend(loc='upper right')
ax3d.view_init(elev=25, azim=-60)
plt.tight_layout()
plt.show()


# ================================================================
#   SAVE STATIC RESULTS
# ================================================================

os.makedirs("results", exist_ok=True)

# --- Save: Damage distribution bar chart ---
fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
seg_names = [f"Segment {i+1}" for i in range(num_segments)]
colors = [get_damage_color(d, failure_threshold) for d in final_damages]
bars = ax_bar.bar(seg_names, final_damages, color=colors, edgecolor='#2c3e50', width=0.6)
ax_bar.axhline(y=failure_threshold, color='red', linewidth=2, linestyle='--', label='Failure Threshold')
for bar, d in zip(bars, final_damages):
    pct = min(d / failure_threshold * 100, 100)
    ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{pct:.0f}%", ha='center', fontsize=12, fontweight='bold')
ax_bar.set_ylabel("Damage Level", fontsize=12)
ax_bar.set_title(f"Final Damage Distribution — After {total_cycles_run} Cycles",
                 fontsize=13, fontweight='bold')
ax_bar.set_ylim(0, max(failure_threshold * 1.2, max(final_damages) * 1.15))
ax_bar.legend(fontsize=10)
ax_bar.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
fig_bar.savefig("results/damage_distribution.png", dpi=150, bbox_inches='tight')
plt.close(fig_bar)

# --- Save: Damage over time ---
fig_time, ax_time = plt.subplots(figsize=(10, 5))
for i in range(num_segments):
    ax_time.plot(history_cycles, history_damages[i], '-', linewidth=2.5,
                 color=seg_colors_line[i % len(seg_colors_line)],
                 label=f'Segment {i+1} (factor: {segment_factors[i]})')
ax_time.axhline(y=failure_threshold, color='red', linewidth=2, linestyle='--',
                label='Failure Threshold', alpha=0.7)
if failure_cycle:
    ax_time.axvline(x=failure_cycle, color='darkred', linewidth=1.5, linestyle='-.',
                    label=f'Failure at Cycle {failure_cycle}', alpha=0.7)
    ax_time.plot(failure_cycle, failure_threshold, 'X', color='darkred', markersize=15, zorder=5)
ax_time.set_xlabel("Load Cycles", fontsize=12)
ax_time.set_ylabel("Damage", fontsize=12)
ax_time.set_title("Fatigue Damage Accumulation Over Load Cycles",
                  fontsize=13, fontweight='bold')
ax_time.legend(fontsize=9)
ax_time.grid(True, alpha=0.3)
ax_time.set_ylim(0, max(failure_threshold * 1.15, max(final_damages) * 1.1))
plt.tight_layout()
fig_time.savefig("results/damage_over_time.png", dpi=150, bbox_inches='tight')
plt.close(fig_time)

print(f"\n  Results saved to results/ folder:")
print(f"    → results/damage_distribution.png")
print(f"    → results/damage_over_time.png")

# --- Summary ---
print(f"\n{'='*55}")
print(f"  SIMULATION SUMMARY")
print(f"{'='*55}")
print(f"  Cycles Run:        {total_cycles_run}")
print(f"  Damage Increment:  {damage_increment}")
print(f"  Failure Threshold: {failure_threshold}")
for i in range(num_segments):
    pct = min(final_damages[i] / failure_threshold * 100, 100)
    status, _ = get_status_text(final_damages[i], failure_threshold)
    print(f"  Segment {i+1}:         {final_damages[i]:.3f} ({pct:.0f}%) — {status}")
print(f"  [!] FAILURE at cycle {failure_cycle}")
print(f"{'='*55}")
