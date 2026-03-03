"""
============================================================
  STRUCTURAL FATIGUE SIMULATION OF A BRIDGE BEAM
  Conceptual / Normalized Model
============================================================

HOW TO USE:
  1. Run: python simulation.py
  2. A settings window will appear — adjust parameters there
  3. Click "Run Simulation" to start
  4. Watch the animated 2D bridge visualization
  5. Close the window → 3D bridge view appears
  6. Close that → summary results are saved as images

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
import tkinter as tk
from tkinter import ttk
import os
import sys

# ================================================================
#   DEFAULT PARAMETERS
# ================================================================

DEFAULT_DAMAGE_INCREMENT = 0.002
DEFAULT_FAILURE_THRESHOLD = 1.0
DEFAULT_ANIMATION_SPEED = 20
DEFAULT_CYCLES_PER_FRAME = 2
DEFAULT_SEGMENT_FACTORS = [0.5, 1.0, 0.5]

num_segments = 3  # Fixed at 3 segments


# ================================================================
#   PARAMETER SETTINGS GUI (Tkinter)
# ================================================================

def show_settings_gui():
    """Display a Tkinter settings window and return user-chosen parameters."""

    result = {}

    def on_run():
        try:
            result['damage_increment'] = float(entry_damage.get())
            result['failure_threshold'] = float(entry_threshold.get())
            result['animation_speed'] = int(entry_anim_speed.get())
            result['cycles_per_frame'] = int(entry_cpf.get())
            result['segment_factors'] = [
                float(entry_factor_left.get()),
                float(entry_factor_center.get()),
                float(entry_factor_right.get()),
            ]
            root.destroy()
        except ValueError:
            error_label.config(text="Invalid input — please enter valid numbers.")

    def on_reset():
        entry_damage.delete(0, tk.END)
        entry_damage.insert(0, str(DEFAULT_DAMAGE_INCREMENT))
        entry_threshold.delete(0, tk.END)
        entry_threshold.insert(0, str(DEFAULT_FAILURE_THRESHOLD))
        entry_anim_speed.delete(0, tk.END)
        entry_anim_speed.insert(0, str(DEFAULT_ANIMATION_SPEED))
        entry_cpf.delete(0, tk.END)
        entry_cpf.insert(0, str(DEFAULT_CYCLES_PER_FRAME))
        entry_factor_left.delete(0, tk.END)
        entry_factor_left.insert(0, str(DEFAULT_SEGMENT_FACTORS[0]))
        entry_factor_center.delete(0, tk.END)
        entry_factor_center.insert(0, str(DEFAULT_SEGMENT_FACTORS[1]))
        entry_factor_right.delete(0, tk.END)
        entry_factor_right.insert(0, str(DEFAULT_SEGMENT_FACTORS[2]))
        slider_damage.set(DEFAULT_DAMAGE_INCREMENT)
        slider_threshold.set(DEFAULT_FAILURE_THRESHOLD)
        error_label.config(text="")

    def on_close():
        sys.exit(0)

    def sync_damage_slider(val):
        entry_damage.delete(0, tk.END)
        entry_damage.insert(0, f"{float(val):.4f}")

    def sync_threshold_slider(val):
        entry_threshold.delete(0, tk.END)
        entry_threshold.insert(0, f"{float(val):.2f}")

    root = tk.Tk()
    root.title("Bridge Fatigue Simulation — Settings")
    root.geometry("520x580")
    root.resizable(False, False)
    root.configure(bg='#f0f0f0')
    root.protocol("WM_DELETE_WINDOW", on_close)

    style = ttk.Style()
    style.theme_use('clam')

    # --- Title ---
    title_frame = tk.Frame(root, bg='#2c3e50', pady=12)
    title_frame.pack(fill='x')
    tk.Label(title_frame, text="Bridge Beam Fatigue Simulation",
             font=('Segoe UI', 14, 'bold'), fg='white', bg='#2c3e50').pack()
    tk.Label(title_frame, text="Configure simulation parameters below",
             font=('Segoe UI', 9), fg='#bdc3c7', bg='#2c3e50').pack()

    # --- Main parameters ---
    param_frame = ttk.LabelFrame(root, text="  Simulation Parameters  ", padding=15)
    param_frame.pack(fill='x', padx=15, pady=(15, 5))

    # Damage Increment
    ttk.Label(param_frame, text="Damage Increment (per cycle):").grid(row=0, column=0, sticky='w', pady=4)
    entry_damage = ttk.Entry(param_frame, width=12)
    entry_damage.insert(0, str(DEFAULT_DAMAGE_INCREMENT))
    entry_damage.grid(row=0, column=1, padx=(10, 5), pady=4)
    slider_damage = ttk.Scale(param_frame, from_=0.0005, to=0.05, orient='horizontal',
                               command=sync_damage_slider, length=150)
    slider_damage.set(DEFAULT_DAMAGE_INCREMENT)
    slider_damage.grid(row=0, column=2, padx=5, pady=4)

    # Failure Threshold
    ttk.Label(param_frame, text="Failure Threshold:").grid(row=1, column=0, sticky='w', pady=4)
    entry_threshold = ttk.Entry(param_frame, width=12)
    entry_threshold.insert(0, str(DEFAULT_FAILURE_THRESHOLD))
    entry_threshold.grid(row=1, column=1, padx=(10, 5), pady=4)
    slider_threshold = ttk.Scale(param_frame, from_=0.1, to=5.0, orient='horizontal',
                                  command=sync_threshold_slider, length=150)
    slider_threshold.set(DEFAULT_FAILURE_THRESHOLD)
    slider_threshold.grid(row=1, column=2, padx=5, pady=4)

    # Animation Speed
    ttk.Label(param_frame, text="Animation Speed (ms/frame):").grid(row=2, column=0, sticky='w', pady=4)
    entry_anim_speed = ttk.Entry(param_frame, width=12)
    entry_anim_speed.insert(0, str(DEFAULT_ANIMATION_SPEED))
    entry_anim_speed.grid(row=2, column=1, padx=(10, 5), pady=4)

    # Cycles per Frame
    ttk.Label(param_frame, text="Cycles per Frame:").grid(row=3, column=0, sticky='w', pady=4)
    entry_cpf = ttk.Entry(param_frame, width=12)
    entry_cpf.insert(0, str(DEFAULT_CYCLES_PER_FRAME))
    entry_cpf.grid(row=3, column=1, padx=(10, 5), pady=4)

    # --- Segment Factors ---
    factor_frame = ttk.LabelFrame(root, text="  Segment Damage Factors  ", padding=15)
    factor_frame.pack(fill='x', padx=15, pady=10)

    ttk.Label(factor_frame, text="Higher factor = more damage per cycle",
              font=('Segoe UI', 8, 'italic')).grid(row=0, column=0, columnspan=3, pady=(0, 8))

    ttk.Label(factor_frame, text="Left Segment:").grid(row=1, column=0, sticky='w', pady=4)
    entry_factor_left = ttk.Entry(factor_frame, width=10)
    entry_factor_left.insert(0, str(DEFAULT_SEGMENT_FACTORS[0]))
    entry_factor_left.grid(row=1, column=1, padx=10, pady=4)

    ttk.Label(factor_frame, text="Center Segment:").grid(row=2, column=0, sticky='w', pady=4)
    entry_factor_center = ttk.Entry(factor_frame, width=10)
    entry_factor_center.insert(0, str(DEFAULT_SEGMENT_FACTORS[1]))
    entry_factor_center.grid(row=2, column=1, padx=10, pady=4)

    ttk.Label(factor_frame, text="Right Segment:").grid(row=3, column=0, sticky='w', pady=4)
    entry_factor_right = ttk.Entry(factor_frame, width=10)
    entry_factor_right.insert(0, str(DEFAULT_SEGMENT_FACTORS[2]))
    entry_factor_right.grid(row=3, column=1, padx=10, pady=4)

    # Hint labels
    ttk.Label(factor_frame, text="(0.1 – 2.0)", font=('Segoe UI', 8)).grid(row=1, column=2, sticky='w')
    ttk.Label(factor_frame, text="(0.1 – 2.0)", font=('Segoe UI', 8)).grid(row=2, column=2, sticky='w')
    ttk.Label(factor_frame, text="(0.1 – 2.0)", font=('Segoe UI', 8)).grid(row=3, column=2, sticky='w')

    # --- Error label ---
    error_label = tk.Label(root, text="", fg='red', bg='#f0f0f0', font=('Segoe UI', 9))
    error_label.pack(pady=(5, 0))

    # --- Buttons ---
    btn_frame = tk.Frame(root, bg='#f0f0f0')
    btn_frame.pack(pady=15)

    run_btn = tk.Button(btn_frame, text="▶  Run Simulation", font=('Segoe UI', 11, 'bold'),
                        bg='#27ae60', fg='white', padx=20, pady=8, relief='flat',
                        activebackground='#2ecc71', cursor='hand2', command=on_run)
    run_btn.grid(row=0, column=0, padx=10)

    reset_btn = tk.Button(btn_frame, text="↺  Reset Defaults", font=('Segoe UI', 10),
                          bg='#7f8c8d', fg='white', padx=15, pady=6, relief='flat',
                          activebackground='#95a5a6', cursor='hand2', command=on_reset)
    reset_btn.grid(row=0, column=1, padx=10)

    # Center the window on screen
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

    if not result:
        sys.exit(0)

    return result


# ================================================================
#   HELPER: Center matplotlib figure on screen
# ================================================================

def center_matplotlib_window(fig):
    """Center a matplotlib figure window on the screen."""
    try:
        backend = plt.get_backend()
        mng = fig.canvas.manager
        if 'Tk' in backend:
            # Get screen dimensions
            fig.canvas.draw()
            win = mng.window
            win.update_idletasks()
            screen_w = win.winfo_screenwidth()
            screen_h = win.winfo_screenheight()
            win_w = win.winfo_width()
            win_h = win.winfo_height()
            x = (screen_w // 2) - (win_w // 2)
            y = (screen_h // 2) - (win_h // 2)
            win.geometry(f'+{x}+{y}')
        elif 'Qt' in backend:
            from PyQt5.QtWidgets import QApplication
            screen = QApplication.primaryScreen().geometry()
            size = mng.window.geometry()
            x = (screen.width() - size.width()) // 2
            y = (screen.height() - size.height()) // 2
            mng.window.move(x, y)
    except Exception:
        pass  # Silently ignore if centering fails


# ================================================================
#   HELPER: Show Retry/Close dialog after simulation
# ================================================================

def show_retry_dialog(summary_text):
    """Show a dialog with simulation summary and Retry/Close buttons.
    Returns True if user wants to retry, False to close."""
    result = {'retry': False}

    dialog = tk.Tk()
    dialog.title("Simulation Complete")
    dialog.geometry("420x320")
    dialog.resizable(False, False)
    dialog.configure(bg='#f0f0f0')

    def on_retry():
        result['retry'] = True
        dialog.destroy()

    def on_close():
        result['retry'] = False
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    # Title bar
    title_frame = tk.Frame(dialog, bg='#2c3e50', pady=10)
    title_frame.pack(fill='x')
    tk.Label(title_frame, text="Simulation Complete",
             font=('Segoe UI', 13, 'bold'), fg='white', bg='#2c3e50').pack()

    # Summary
    summary_frame = tk.Frame(dialog, bg='#f0f0f0', pady=10, padx=15)
    summary_frame.pack(fill='both', expand=True)

    summary_label = tk.Label(summary_frame, text=summary_text,
                              font=('Consolas', 9), fg='#2c3e50', bg='#ecf0f1',
                              justify='left', anchor='w', padx=10, pady=8,
                              relief='groove')
    summary_label.pack(fill='both', expand=True)

    # Buttons
    btn_frame = tk.Frame(dialog, bg='#f0f0f0', pady=12)
    btn_frame.pack(fill='x')

    retry_btn = tk.Button(btn_frame, text="\u21ba  Retry (Edit Parameters)",
                          font=('Segoe UI', 11, 'bold'),
                          bg='#2980b9', fg='white', padx=18, pady=8,
                          relief='flat', activebackground='#3498db',
                          cursor='hand2', command=on_retry)
    retry_btn.pack(side='left', padx=(40, 10))

    close_btn = tk.Button(btn_frame, text="\u2716  Close",
                          font=('Segoe UI', 11, 'bold'),
                          bg='#c0392b', fg='white', padx=18, pady=8,
                          relief='flat', activebackground='#e74c3c',
                          cursor='hand2', command=on_close)
    close_btn.pack(side='right', padx=(10, 40))

    # Center dialog on screen
    dialog.update_idletasks()
    w = dialog.winfo_width()
    h = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (w // 2)
    y = (dialog.winfo_screenheight() // 2) - (h // 2)
    dialog.geometry(f'+{x}+{y}')

    dialog.mainloop()
    return result['retry']



# ================================================================
#   HELPER FUNCTIONS
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
#   MAIN SIMULATION LOOP (with retry support)
# ================================================================

while True:
    params = show_settings_gui()

    damage_increment = params['damage_increment']
    failure_threshold = params['failure_threshold']
    animation_speed = params['animation_speed']
    cycles_per_frame = params['cycles_per_frame']
    segment_factors = params['segment_factors']

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
    #   ANIMATED 2D VISUALIZATION — Enhanced Bridge Design
    # ================================================================

    print("  Opening animated 2D bridge visualization...")

    fig = plt.figure(figsize=(16, 11))
    fig.patch.set_facecolor('#e8f4f8')
    gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.30,
                  height_ratios=[3.0, 0.55, 0.7])

    # Title
    fig.suptitle("Structural Fatigue Simulation of a Bridge Beam",
                 fontsize=16, fontweight='bold', y=0.98, color='#2c3e50')

    # --- Top row: Enhanced Bridge visualization (LARGE) ---
    ax_beam = fig.add_subplot(gs[0, :])
    ax_beam.set_xlim(-2.0, num_segments + 2.0)
    ax_beam.set_ylim(-2.8, 3.8)
    ax_beam.set_aspect('equal')
    ax_beam.axis('off')
    ax_beam.set_facecolor('#d4eaf7')

    ax_beam.set_title("Bridge Beam — Structural View", fontsize=12,
                       fontweight='bold', color='#2c3e50')

    # ---- Draw sky gradient (background) ----
    for i in range(20):
        y_start = 1.8 + i * 0.085
        alpha_val = 0.08 - i * 0.003
        if alpha_val > 0:
            ax_beam.axhspan(y_start, y_start + 0.085, color='#87CEEB', alpha=alpha_val)

    # ---- Draw water/ground underneath ----
    water = mpatches.FancyBboxPatch((-1.5, -2.5), num_segments + 3, 1.8,
                                     boxstyle="square", facecolor='#5dade2',
                                     edgecolor='none', alpha=0.25)
    ax_beam.add_patch(water)
    # Water ripples
    for wx in np.linspace(-1.0, num_segments + 1.0, 8):
        ax_beam.plot([wx - 0.15, wx + 0.15], [-1.2, -1.2], color='#3498db',
                     linewidth=1, alpha=0.4)
    ax_beam.text(num_segments / 2, -1.8, '~ Water Level ~', ha='center',
                 fontsize=7, color='#2980b9', fontstyle='italic', alpha=0.6)

    # ---- Draw support piers (concrete columns) ----
    pier_width = 0.35
    pier_color = '#95a5a6'
    pier_edge = '#7f8c8d'

    # Left pier
    left_pier = mpatches.FancyBboxPatch((-pier_width / 2, -1.5), pier_width, 1.55,
                                         boxstyle="round,pad=0.02",
                                         facecolor=pier_color, edgecolor=pier_edge,
                                         linewidth=1.5)
    ax_beam.add_patch(left_pier)
    # Pier cap (wider top)
    left_cap = mpatches.FancyBboxPatch((-pier_width / 2 - 0.1, -0.05), pier_width + 0.2, 0.12,
                                        boxstyle="round,pad=0.01",
                                        facecolor='#7f8c8d', edgecolor=pier_edge, linewidth=1)
    ax_beam.add_patch(left_cap)
    # Pier base
    left_base = mpatches.FancyBboxPatch((-pier_width / 2 - 0.15, -1.55), pier_width + 0.3, 0.12,
                                         boxstyle="round,pad=0.01",
                                         facecolor='#7f8c8d', edgecolor=pier_edge, linewidth=1)
    ax_beam.add_patch(left_base)

    # Right pier
    right_pier = mpatches.FancyBboxPatch((num_segments - pier_width / 2, -1.5),
                                          pier_width, 1.55,
                                          boxstyle="round,pad=0.02",
                                          facecolor=pier_color, edgecolor=pier_edge,
                                          linewidth=1.5)
    ax_beam.add_patch(right_pier)
    right_cap = mpatches.FancyBboxPatch((num_segments - pier_width / 2 - 0.1, -0.05),
                                         pier_width + 0.2, 0.12,
                                         boxstyle="round,pad=0.01",
                                         facecolor='#7f8c8d', edgecolor=pier_edge, linewidth=1)
    ax_beam.add_patch(right_cap)
    right_base = mpatches.FancyBboxPatch((num_segments - pier_width / 2 - 0.15, -1.55),
                                          pier_width + 0.3, 0.12,
                                          boxstyle="round,pad=0.01",
                                          facecolor='#7f8c8d', edgecolor=pier_edge, linewidth=1)
    ax_beam.add_patch(right_base)

    # ---- Draw road deck (asphalt surface on top) ----
    deck_y = 0.8
    deck_h = 0.18
    road_deck = mpatches.FancyBboxPatch((-0.3, deck_y), num_segments + 0.6, deck_h,
                                         boxstyle="round,pad=0.02",
                                         facecolor='#515a5a', edgecolor='#2c3e50',
                                         linewidth=1.5)
    ax_beam.add_patch(road_deck)

    # Road dashed center line
    for dx in np.arange(0.1, num_segments - 0.1, 0.35):
        ax_beam.plot([dx, dx + 0.18], [deck_y + deck_h / 2, deck_y + deck_h / 2],
                     color='#f1c40f', linewidth=2, solid_capstyle='round')

    # Road edge lines
    ax_beam.plot([-0.25, num_segments + 0.25], [deck_y + 0.02, deck_y + 0.02],
                 color='white', linewidth=1, alpha=0.8)
    ax_beam.plot([-0.25, num_segments + 0.25], [deck_y + deck_h - 0.02, deck_y + deck_h - 0.02],
                 color='white', linewidth=1, alpha=0.8)

    # ---- Draw railings ----
    railing_h = 0.35
    railing_y = deck_y + deck_h
    # Left railing
    for rx in np.linspace(-0.2, num_segments + 0.2, 12):
        ax_beam.plot([rx, rx], [railing_y, railing_y + railing_h],
                     color='#7f8c8d', linewidth=1.2, alpha=0.7)
    ax_beam.plot([-0.2, num_segments + 0.2], [railing_y + railing_h, railing_y + railing_h],
                 color='#566573', linewidth=2)

    # ---- Beam segments (structural girders below deck) ----
    seg_patches = []
    seg_texts = []
    seg_label_texts = []
    seg_crack_lines = []

    for i in range(num_segments):
        # Main beam girder
        rect = mpatches.FancyBboxPatch((i + 0.03, 0.05), 0.94, 0.73,
                                        boxstyle="round,pad=0.02",
                                        facecolor='#2ecc71', edgecolor='#2c3e50',
                                        linewidth=2)
        ax_beam.add_patch(rect)
        seg_patches.append(rect)

        # Segment damage percentage text
        txt = ax_beam.text(i + 0.5, 0.42, "0.0%", ha='center', va='center',
                           fontsize=12, fontweight='bold', color='white',
                           bbox=dict(boxstyle='round,pad=0.1', facecolor='none',
                                     edgecolor='none'))
        seg_texts.append(txt)

        # Segment label
        lbl = ax_beam.text(i + 0.5, -0.12, f"Segment {i+1}\n({'Left' if i == 0 else 'Center' if i == 1 else 'Right'})",
                           ha='center', fontsize=7, color='#2c3e50', fontweight='bold')
        seg_label_texts.append(lbl)

        # Stiffener lines on girder (structural detail)
        for sy in [0.25, 0.55]:
            ax_beam.plot([i + 0.08, i + 0.92], [sy, sy],
                         color='#2c3e50', linewidth=0.5, alpha=0.3)

    # ---- Load arrow (traffic load) ----
    mid = num_segments / 2
    ax_beam.annotate('', xy=(mid, railing_y + railing_h + 0.05),
                     xytext=(mid, railing_y + railing_h + 0.7),
                     arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=3,
                                     connectionstyle='arc3'))
    ax_beam.text(mid, railing_y + railing_h + 0.8, 'Repeated Load (Traffic)',
                 ha='center', fontsize=10, fontweight='bold', color='#e74c3c')

    # Small vehicle icon on road
    vehicle_x = mid - 0.2
    vehicle_y = deck_y + 0.03
    vehicle = mpatches.FancyBboxPatch((vehicle_x, vehicle_y), 0.4, 0.12,
                                       boxstyle="round,pad=0.02",
                                       facecolor='#e74c3c', edgecolor='#c0392b',
                                       linewidth=1, alpha=0.7)
    ax_beam.add_patch(vehicle)

    # --- Middle row: Compact indicators (gauge, status, info, chart) ---

    # Damage gauge (compact)
    ax_gauge = fig.add_subplot(gs[1, 0])
    ax_gauge.set_title("Damage", fontsize=8, fontweight='bold', color='#2c3e50', pad=2)
    ax_gauge.set_xlim(0, 1)
    ax_gauge.set_ylim(0, 1.1)
    ax_gauge.set_xticks([])
    ax_gauge.set_yticks([])

    gauge_bg = mpatches.FancyBboxPatch((0.1, 0.05), 0.8, 0.8,
                                        boxstyle="round,pad=0.03",
                                        facecolor='#ecf0f1', edgecolor='#bdc3c7', lw=1.5)
    ax_gauge.add_patch(gauge_bg)

    gauge_fill = mpatches.Rectangle((0.2, 0.1), 0.6, 0.0,
                                     facecolor='#2ecc71', edgecolor='none')
    ax_gauge.add_patch(gauge_fill)

    gauge_border = mpatches.Rectangle((0.2, 0.1), 0.6, 0.65,
                                       facecolor='none', edgecolor='#2c3e50', lw=1.5)
    ax_gauge.add_patch(gauge_border)

    ax_gauge.plot([0.17, 0.83], [0.1 + 0.65, 0.1 + 0.65], 'r--', lw=1.5)
    ax_gauge.text(0.5, 0.78, 'FAIL', ha='center', fontsize=6, color='red', fontweight='bold')

    gauge_pct_text = ax_gauge.text(0.5, 0.93, "0%", ha='center', fontsize=14, fontweight='bold', color='#2c3e50')

    # Beam Status (compact)
    ax_status = fig.add_subplot(gs[1, 1])
    ax_status.set_xlim(0, 1)
    ax_status.set_ylim(0, 1)
    ax_status.set_xticks([])
    ax_status.set_yticks([])
    ax_status.set_title("Status", fontsize=8, fontweight='bold', color='#2c3e50', pad=2)

    status_bg = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                                         boxstyle="round,pad=0.05",
                                         facecolor='#2ecc71', edgecolor='#2c3e50', lw=1.5)
    ax_status.add_patch(status_bg)
    status_text = ax_status.text(0.5, 0.55, "SAFE", ha='center', va='center',
                                  fontsize=16, fontweight='bold', color='white')
    status_bullet_1 = ax_status.text(0.12, 0.28, "\u25cf SAFE", fontsize=6, color='white')
    status_bullet_2 = ax_status.text(0.12, 0.18, "\u25cf WARNING", fontsize=6, color='white')
    status_bullet_3 = ax_status.text(0.55, 0.28, "\u25cf CRITICAL", fontsize=6, color='white')
    status_bullet_4 = ax_status.text(0.55, 0.18, "\u25cf FAILED", fontsize=6, color='white')

    # Cycle counter (compact)
    ax_info = fig.add_subplot(gs[1, 2])
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.set_xticks([])
    ax_info.set_yticks([])
    ax_info.set_title("Info", fontsize=8, fontweight='bold', color='#2c3e50', pad=2)

    info_bg = mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                       boxstyle="round,pad=0.05",
                                       facecolor='#ecf0f1', edgecolor='#bdc3c7', lw=1.5)
    ax_info.add_patch(info_bg)

    cycle_text = ax_info.text(0.5, 0.8, "Cycle: 0", ha='center', fontsize=11, fontweight='bold', color='#2c3e50')
    param_texts = [
        ax_info.text(0.1, 0.6, f"Dmg/Cycle: {damage_increment}", fontsize=7, color='#7f8c8d'),
        ax_info.text(0.1, 0.45, f"Threshold: {failure_threshold}", fontsize=7, color='#7f8c8d'),
        ax_info.text(0.1, 0.3, f"Segments: {num_segments}", fontsize=7, color='#7f8c8d'),
        ax_info.text(0.1, 0.15, f"Factors: {segment_factors}", fontsize=7, color='#7f8c8d'),
    ]

    # Segment detail panel (compact) — new 4th column
    ax_seg_detail = fig.add_subplot(gs[1, 3])
    ax_seg_detail.set_xlim(0, 1)
    ax_seg_detail.set_ylim(0, 1)
    ax_seg_detail.set_xticks([])
    ax_seg_detail.set_yticks([])
    ax_seg_detail.set_title("Segments", fontsize=8, fontweight='bold', color='#2c3e50', pad=2)

    seg_detail_bg = mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                             boxstyle="round,pad=0.05",
                                             facecolor='#ecf0f1', edgecolor='#bdc3c7', lw=1.5)
    ax_seg_detail.add_patch(seg_detail_bg)

    seg_detail_texts = []
    for si in range(num_segments):
        seg_name = ['Left', 'Center', 'Right'][si]
        sdt = ax_seg_detail.text(0.5, 0.75 - si * 0.28, f"S{si+1} ({seg_name}): 0.0%",
                                  ha='center', fontsize=8, fontweight='bold', color='#2c3e50')
        seg_detail_texts.append(sdt)

    # --- Bottom row: Damage over time chart (compact) ---
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

    def animate(frame_idx, direct_idx=False):
        if direct_idx:
            idx = frame_idx
        else:
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
        fill_height = min(max_d / failure_threshold, 1.0) * 0.65
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

        # Update segment detail panel
        for si in range(num_segments):
            d_si = history_damages[si][idx]
            pct_si = min(d_si / failure_threshold * 100, 100)
            seg_name = ['Left', 'Center', 'Right'][si]
            st_lbl, _ = get_status_text(d_si, failure_threshold)
            seg_detail_texts[si].set_text(f"S{si+1} ({seg_name}): {pct_si:.0f}% {st_lbl}")

        # Update chart lines
        for i in range(num_segments):
            lines[i].set_data(history_cycles[:idx+1], history_damages[i][:idx+1])

        return seg_patches + seg_texts + [gauge_fill, gauge_pct_text, status_bg, status_text, cycle_text] + seg_detail_texts + lines

    num_frames = (total_frames + cycles_per_frame - 1) // cycles_per_frame + 1

    def animate_wrapper(frame_idx):
        # Ensure the very last frame always shows the final cycle
        if frame_idx >= num_frames - 1:
            return animate(total_frames - 1, direct_idx=True)
        return animate(frame_idx)

    anim = animation.FuncAnimation(fig, animate_wrapper, frames=num_frames,
                                    interval=animation_speed, blit=False, repeat=False)

    try:
        fig.tight_layout(rect=[0, 0, 1, 0.95])
    except Exception:
        pass  # tight_layout may warn with mixed axes
    center_matplotlib_window(fig)
    plt.show()

    # ================================================================
    #   SAVE STATIC RESULTS
    # ================================================================

    final_damages = [history_damages[i][-1] for i in range(num_segments)]
    total_cycles_run = history_cycles[-1]

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
    ax_bar.set_title(f"Final Damage Distribution \u2014 After {total_cycles_run} Cycles",
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
    print(f"    \u2192 results/damage_distribution.png")
    print(f"    \u2192 results/damage_over_time.png")

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
        print(f"  Segment {i+1}:         {final_damages[i]:.3f} ({pct:.0f}%) \u2014 {status}")
    print(f"  [!] FAILURE at cycle {failure_cycle}")
    print(f"{'='*55}")

    # --- Retry / Close dialog ---
    summary_lines = [
        f"Cycles Run: {total_cycles_run}",
        f"Damage Increment: {damage_increment}",
        f"Failure Threshold: {failure_threshold}",
        "",
    ]
    for i in range(num_segments):
        pct = min(final_damages[i] / failure_threshold * 100, 100)
        st, _ = get_status_text(final_damages[i], failure_threshold)
        summary_lines.append(f"Segment {i+1}: {final_damages[i]:.3f} ({pct:.0f}%) \u2014 {st}")
    summary_lines.append(f"\nFAILURE at cycle {failure_cycle}")
    summary_str = "\n".join(summary_lines)

    if not show_retry_dialog(summary_str):
        print("\n  Simulation closed. Goodbye!")
        break
    else:
        print("\n  Retrying with new parameters...\n")
