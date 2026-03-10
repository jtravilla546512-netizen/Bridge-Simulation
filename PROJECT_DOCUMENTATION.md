# A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

## Project Documentation (Normalized / Conceptual Model)

---

## 1. Introduction

Modeling and Simulation is a computational technique used to represent and analyze real-world systems without the need for costly physical experiments or disrupting actual operations. It is especially valuable in structural engineering, where physical testing of full-scale structures such as bridges is impractical, expensive, and potentially dangerous. By creating computational models of structural behavior, engineers and researchers can predict how components respond to various loading conditions over time, enabling better decision-making regarding maintenance, design, and safety.

Structural fatigue — the progressive weakening of a material subjected to repeated (cyclic) loading — is one of the leading causes of bridge failures worldwide. Even when individual load cycles are well below the material's ultimate strength, the cumulative effect of thousands of loading cycles can eventually lead to catastrophic failure. Understanding this invisible degradation process is critical for infrastructure safety.

This project focuses on developing a **Python-based conceptual simulation** of structural fatigue in bridge beams under repeated loading. The simulation uses a **normalized damage accumulation model** (based on Miner's Rule) to demonstrate the core principles of fatigue behavior. It models a bridge beam divided into 3 segments (left, center, right), applies cyclic damage based on position-dependent vulnerability factors, tracks damage accumulation at each segment in real time, and presents results through an **enhanced animated 2D bridge visualization** with interactive controls. The system features an **interactive Tkinter settings GUI** for parameter adjustment before each run and a **retry/close dialog** after completion, allowing users to perform multiple simulation runs with different parameters to compare outcomes and support data-driven decisions.

---

## 2. Problem Description

Bridge beams are subjected to repeated loading from vehicular traffic throughout their operational life. Each load cycle, while individually harmless, contributes incrementally to fatigue damage within the structural material. Over time, this accumulated damage can reach the structure's fatigue limit — often without visible warning signs until it is too late.

The key problems motivating this study include:

- **Fatigue is invisible in early stages.** Damage accumulates gradually beneath the surface and cannot be detected by visual inspection until the structure is already compromised. Engineers and decision-makers need tools to visualize this hidden process.
- **Physical testing is impractical and costly.** Full-scale fatigue testing of bridges requires expensive equipment, significant time, and risks damaging the actual structure. Simulation provides a safe, repeatable, and cost-effective alternative.
- **Predictive capability is needed for maintenance planning.** Infrastructure managers need to estimate the remaining fatigue life of bridge components to schedule maintenance and allocate budgets effectively. Without simulation, these decisions rely on guesswork.
- **Position-dependent vulnerability is not intuitive.** Different parts of a bridge beam experience different levels of stress — the center (midspan) is most vulnerable while sections near supports are more protected. This spatial variation needs to be demonstrated clearly.
- **Parameter sensitivity is difficult to assess manually.** Understanding how changes in damage rate, material threshold, or structural design affect fatigue life requires running multiple scenarios — something that is only practical through simulation.

A simulation approach allows us to model damage accumulation, predict when the fatigue limit is reached, visualize the progressive degradation process, and test different scenarios — all computationally and without any risk to real infrastructure.

**Important:** This simulation does **not** predict whether a bridge will collapse or break. Instead, it **visualizes how structural fatigue accumulates over time** under repeated loading. It shows the progression of damage — not the moment of collapse.

---

## 3. Objectives

The objectives of this simulation study are:

1. To **simulate cumulative fatigue damage** using a cycle-based model that tracks damage across 3 beam segments (left, center, right) under repeated cyclic loading
2. To **model position-dependent vulnerability** using segment factors — specifically identifying that the center segment (midspan) accumulates damage fastest due to its higher vulnerability factor (1.0) compared to edge segments (0.5)
3. To **detect and report structural failure** when any segment's accumulated fatigue reaches the failure threshold, stopping the simulation and reporting results
4. To **provide real-time animated 2D visualization** of the bridge showing color-coded segment status transitions (SAFE → LOW DAMAGE → WARNING → CRITICAL → FAILURE) with a damage gauge, status panel, segment details, and damage-over-time chart
5. To **enable parameter experimentation** via an interactive Tkinter GUI settings window — allowing users to adjust damage increment, failure threshold, animation speed, cycles per frame, and per-segment vulnerability factors without editing code

---

## 4. System Description

The system represents a simply-supported bridge beam subjected to repeated traffic loading. The following components define the system:

### Entities

| Entity | Description |
|--------|-------------|
| **Bridge Beam** | The primary structural element being simulated — a simply-supported beam resting on two piers |
| **Beam Segments** | The beam is divided into 3 segments: Segment 1 (Left, near support), Segment 2 (Center, at midspan), and Segment 3 (Right, near support). Each segment tracks its own independent damage state |
| **Load Cycles** | Repeated loading events representing vehicular traffic crossing the bridge. Each cycle (one vehicle passing) applies a fixed damage increment to every segment, scaled by its position-dependent factor |
| **Fatigue Damage State** | Damage level per segment, from 0.0 (no damage) to the failure threshold (default: 1.0 = full fatigue capacity reached) |

### Resources

| Resource | Description |
|----------|-------------|
| **Segment Damage Capacity** | Each segment can absorb damage from 0.0 (undamaged) up to the failure threshold (default: 1.0). Once a segment's accumulated damage reaches the threshold, the fatigue limit has been reached |
| **Structural Integrity** | The overall beam remains operational as long as no segment has reached the failure threshold. When the most critical segment (center) reaches its fatigue limit, the entire bridge has reached its structural fatigue limit — because a structure is only as strong as its weakest section |

### Events

| Event | Description |
|-------|-------------|
| **Load Application** | Each cycle applies damage: `damage += damage_increment × segment_factor` to every segment simultaneously |
| **Status Transition** | As damage accumulates, each segment transitions through 5 states: SAFE (0–24%) → LOW DAMAGE (25–49%) → WARNING (50–74%) → CRITICAL (75–99%) → FAILURE (100%) |
| **Failure Detection** | When any segment's accumulated damage reaches or exceeds the failure threshold, the simulation records the failure cycle and stops the loading loop |
| **Simulation Completion** | After failure is detected, the visualization plays back the full damage history, results are saved, and the user is presented with a summary |

### System Flow

Load cycles arrive deterministically — one cycle per iteration. Each cycle simultaneously applies damage to all 3 segments based on their individual vulnerability factors. The center segment (factor: 1.0) accumulates damage twice as fast as the edge segments (factor: 0.5), making it the first to reach the fatigue limit. The simulation runs continuously until the fatigue limit is reached (no fixed cycle limit). After completion, the user can retry with different parameters or exit.

### Why the Entire Bridge Is Considered to Have Reached Its Fatigue Limit

When only the center segment reaches 100% while the left and right segments are at 50%, the overall bridge is still considered to have reached its **structural fatigue limit**. This is because:

- The center segment is the **most critical part** of the bridge — it carries the most stress
- A bridge is like a **chain** — it is only as strong as its weakest link
- If the center's fatigue capacity is fully consumed, the bridge **cannot safely carry traffic anymore**, even if the edges still have remaining capacity
- In real-world structural engineering, when the **most vulnerable component** has accumulated full fatigue damage, the **entire structure is no longer safe to use**

---

## 5. Model Design

The simulation model is implemented in Python using Tkinter for the GUI and Matplotlib for visualization. The model is structured using the following components:

### Modules / Components

| Module | Implementation | Purpose |
|--------|---------------|---------|
| **Settings GUI** (`show_settings_gui()`) | Tkinter window with text entries, sliders, and buttons | Allows users to configure all simulation parameters before each run: damage increment, failure threshold, animation speed, cycles per frame, and per-segment vulnerability factors |
| **Simulation Engine** (main `while True` loop) | Pure Python computation with NumPy | Executes the damage accumulation loop: initializes 3 segments at 0.0 damage, applies `damage += damage_increment × segment_factor` each cycle, checks for failure, and records full history |
| **Animated 2D Visualization** (`matplotlib.animation`) | Matplotlib figure with GridSpec layout (3 rows × 4 columns) | Plays back the simulation results as an animation showing: the bridge structure (piers, road deck, railings, water, vehicle icon), color-coded beam segments, max damage gauge with zone bands, color-coded status panel, segment detail panel with individual status indicators, and damage-over-time chart |
| **Static Results Export** | Matplotlib figures saved as PNG | Generates and saves `damage_distribution.png` (bar chart) and `damage_over_time.png` (line plot) to the `results/` folder |
| **Retry/Close Dialog** (`show_retry_dialog()`) | Tkinter dialog | Displays a summary of simulation results and offers the user the choice to retry with new parameters or close the application |

### Entity Flow

```
Settings GUI → Configure Parameters → Run Simulation Engine
    → Accumulate Damage Per Cycle → Detect Failure
    → Animated 2D Playback → Save Result Images
    → Retry/Close Dialog → [Retry → Settings GUI] or [Close → Exit]
```

### Core Algorithm

```python
# Initialize
beam_segments = [0.0, 0.0, 0.0]  # 3 segments, all starting at zero damage

# Simulation loop — runs until failure
cycle = 0
while True:
    cycle += 1
    for i in range(3):
        beam_segments[i] += damage_increment * segment_factors[i]

    # Check failure
    for i in range(3):
        if beam_segments[i] >= failure_threshold:
            failure_cycle = cycle  # Record and stop
            break
```

### Fatigue Formula

```
damage += damage_increment × segment_factor
```

The number of cycles to reach the fatigue limit can be predicted:

$$N_f = \frac{\text{failure\_threshold}}{\text{damage\_increment} \times \max(\text{segment\_factors})}$$

With defaults: $N_f = \frac{1.0}{0.002 \times 1.0} = 500$ cycles.

### Color Status System (5 Levels)

| Damage Ratio (damage / threshold) | Status | Visual Color |
|-----------------------------------|--------|-------------|
| 0% – 24% | SAFE | Green (#2ecc71) |
| 25% – 49% | LOW DAMAGE | Yellow (#f1c40f) |
| 50% – 74% | WARNING | Orange (#e67e22) |
| 75% – 99% | CRITICAL | Red (#e74c3c) |
| 100% | FAILURE | Dark Red (#8e0000) |

---

## 6. Assumptions

The following assumptions simplify the model and must be clearly understood:

- **Linear damage accumulation.** Damage grows linearly each cycle: `D += damage_increment × segment_factor`. There is no acceleration, deceleration, or non-linear fatigue curve (e.g., no S-N curve modeling)
- **Deterministic loading.** Every load cycle applies the exact same damage increment — there is no randomness or variation in load magnitude. This is a fixed-increment model, not a stochastic one
- **Fixed segment vulnerability factors.** Position-dependent damage multipliers remain constant throughout the simulation (default: Left = 0.5, Center = 1.0, Right = 0.5). They do not change as damage accumulates
- **Independent segments.** Damage in one segment does not influence or propagate to neighboring segments. Each segment is tracked independently
- **Irreversible damage.** Damage can only increase, never decrease. There is no repair, recovery, or healing mechanism
- **Single failure threshold.** All segments share the same failure threshold (default: 1.0). The fatigue limit is reached when **any** segment reaches this value — the bridge is only as strong as its weakest section
- **No environmental factors.** Temperature, corrosion, humidity, wind, and other environmental effects are not modeled
- **No geometric changes.** The beam geometry and cross-section remain unchanged throughout the simulation regardless of damage level
- **Simply-supported beam.** The beam is supported at both ends (left and right piers) with load applied at the center
- **Normalized / conceptual model.** All values are unitless and normalized (0.0 to 1.0). This is an educational model, not a certified engineering calculation
- **The simulation shows fatigue accumulation, not structural collapse.** It visualizes the process of damage building up — not the moment of failure

---

## 7. Simulation Setup

### Run Configuration

| Setting | Value |
|---------|-------|
| **Run mode** | Run until fatigue limit is reached (no fixed cycle limit) |
| **Termination condition** | Any segment's damage ≥ failure threshold |
| **Number of replications** | User-controlled via Retry dialog — can run as many times as desired with different parameters |
| **Console output frequency** | Every 50 cycles (plus cycle 1) |

### Configurable Parameters (via GUI)

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Damage Increment | 0.002 | 0.0005 – 0.05 (slider) | Normalized damage added per cycle before applying segment factor |
| Failure Threshold | 1.0 | 0.1 – 5.0 (slider) | Damage level at which a segment's fatigue capacity is fully consumed |
| Animation Speed | 20 ms | Any positive integer | Milliseconds between animation frames (lower = faster) |
| Cycles per Frame | 2 | Any positive integer | Number of load cycles advanced per animation frame |
| Left Segment Factor | 0.5 | 0.1 – 2.0 | Damage multiplier for Segment 1 (near left support) |
| Center Segment Factor | 1.0 | 0.1 – 2.0 | Damage multiplier for Segment 2 (at midspan) |
| Right Segment Factor | 0.5 | 0.1 – 2.0 | Damage multiplier for Segment 3 (near right support) |

### Performance Measures Collected

| Measure | Description |
|---------|-------------|
| **Cycles to failure** | The exact cycle number when the first segment reaches the failure threshold |
| **Final damage per segment** | The accumulated damage value for each of the 3 segments at the time of failure |
| **Damage percentage per segment** | Each segment's damage expressed as a percentage of the failure threshold |
| **Segment status at failure** | The status classification (SAFE / LOW DAMAGE / WARNING / CRITICAL / FAILURE) for each segment |
| **Maximum damage** | The highest damage value reached by any segment (equals the failure threshold) |
| **Damage history over time** | Full cycle-by-cycle damage record for each segment, used for the time-series chart |

---

## 8. Results and Analysis

### Default Parameter Results

Using the default parameters (`damage_increment = 0.002`, `failure_threshold = 1.0`, `segment_factors = [0.5, 1.0, 0.5]`), the simulation produces the following results:

| Segment | Position | Factor | Final Damage | Percentage | Status |
|---------|----------|--------|-------------|-----------|--------|
| Segment 1 | Left (near support) | 0.5 | 0.500 | 50% | WARNING |
| Segment 2 | Center (midspan) | 1.0 | 1.000 | 100% | **FAILURE** |
| Segment 3 | Right (near support) | 0.5 | 0.500 | 50% | WARNING |

**Key findings:**

- **Fatigue limit reached at cycle 500.** Segment 2 (center) is the first to reach the failure threshold because its vulnerability factor (1.0) is twice that of the edge segments (0.5)
- **Edge segments reach exactly 50% damage** at the point of center failure — mathematically consistent with their half-factor: `500 cycles × 0.002 × 0.5 = 0.500`
- **The center is always the critical segment** under the default configuration, confirming that midspan positions are most vulnerable in a simply-supported beam
- **The overall bridge has reached its structural fatigue limit** even though only the center is at 100% — because the most critical section of the beam can no longer safely carry traffic (the bridge is only as strong as its weakest segment)

### Replication Runs (4 Runs with Different Parameters)

By varying one parameter at a time using the Settings GUI and Retry feature, the following results were observed:

| Run | What Changed | Damage Inc. | Threshold | Factors | Cycles to Failure | Which Segment |
|-----|-------------|------------|-----------|---------|-------------------|---------------|
| **1 (Baseline)** | Default | 0.002 | 1.0 | [0.5, 1.0, 0.5] | **500** | Center |
| **2 (Double Dmg)** | ×2 damage | 0.004 | 1.0 | [0.5, 1.0, 0.5] | **250** | Center |
| **3 (Half Dmg)** | ½ damage | 0.001 | 1.0 | [0.5, 1.0, 0.5] | **1000** | Center |
| **4 (High Thresh)** | ×2 threshold | 0.002 | 2.0 | [0.5, 1.0, 0.5] | **1000** | Center |

### Cross-Run Validation

All 4 runs match the fatigue life formula exactly:

$$N_f = \frac{\text{failure\_threshold}}{\text{damage\_increment} \times \max(\text{segment\_factors})}$$

| Run | Formula Prediction | Actual Result | Match |
|-----|-------------------|---------------|-------|
| 1 | 1.0 / (0.002 × 1.0) = 500 | 500 | ✅ |
| 2 | 1.0 / (0.004 × 1.0) = 250 | 250 | ✅ |
| 3 | 1.0 / (0.001 × 1.0) = 1000 | 1000 | ✅ |
| 4 | 2.0 / (0.002 × 1.0) = 1000 | 1000 | ✅ |

**4 out of 4 predictions match → Model is validated.**

### Analysis

- **Damage rate and fatigue life are inversely proportional.** Doubling the damage rate halves the number of survivable cycles (Run 2: 500→250). Halving the damage rate doubles the fatigue life (Run 3: 500→1000). This is the most sensitive parameter — small changes produce large effects on structural lifespan
- **Failure threshold and fatigue life are directly proportional.** Doubling the threshold doubles the survivable cycles (Run 4: 500→1000), simulating a stronger or more damage-tolerant material
- **Segment factors control the spatial distribution of damage.** The center segment (factor=1.0) always reaches the fatigue limit first because it accumulates damage twice as fast as the edges (factor=0.5). The factor ratio determines which segment fails first
- **The simulation correctly implements Miner's Rule.** All results are mathematically predictable and match the formula exactly across all 4 replication runs
- **The center always fails first** — and when it does, the entire bridge has reached its structural fatigue limit, because a structure is only as safe as its most critical section

### Output Visualizations

The simulation generates the following outputs automatically:

1. **Animated 2D bridge visualization** — Real-time playback showing the bridge structure with color-coded beam segments transitioning through 5 status levels (green→yellow→orange→red→dark red), a max damage gauge with color zone bands, a color-coded status panel with legend, segment detail panel with individual indicators, and a live damage-over-time chart
2. **`results/damage_distribution.png`** — Bar chart showing the final damage level of each segment with color coding and percentage labels
3. **`results/damage_over_time.png`** — Line plot showing the damage accumulation trajectory of each segment over all load cycles, with the failure threshold and failure point marked

---

## 9. Recommendations

Based on the simulation results and analysis of 4 replication runs, the following recommendations are made:

### For Using This Simulation

- **Always start with default parameters first.** The defaults (increment=0.002, threshold=1.0, factors=[0.5, 1.0, 0.5]) produce a clean 500-cycle baseline run. Understand this first, then modify one parameter at a time
- **Change only one parameter at a time.** This isolates the effect of each parameter — the standard scientific approach for deterministic simulation analysis
- **Use the Retry feature for experimentation.** After each run, the dialog lets you return to the GUI and test new values without restarting the program

### For Future Improvements

1. **Add variable loading (random traffic).** Currently every cycle applies the same damage. In real life, a motorcycle and a heavy truck put very different stress on a bridge. Adding randomness (normal distribution for load per cycle) would make the model stochastic, requiring 20–30 replications per configuration for statistical analysis
2. **Add more than 3 segments.** A real bridge can be divided into 10–20 segments for finer resolution, allowing engineers to pinpoint exact fatigue zones instead of just general areas
3. **Add non-linear damage accumulation.** Miner's Rule assumes linear damage, but real fatigue starts slow and accelerates near end-of-life. The bridge might look fine for 80% of its life, then deteriorate rapidly in the last 20% — a non-linear model (S-curve or exponential) would capture this dangerous behavior

---

## 10. Conclusion

This project successfully demonstrated the use of computational simulation to model and analyze structural fatigue in a bridge beam under repeated loading. Using a normalized damage accumulation model (Miner's Rule) implemented in Python, the simulation tracked how cumulative cyclic loading leads to progressive degradation and eventual reaching of the fatigue limit — with the center (midspan) segment consistently identified as the most vulnerable point.

The simulation model provided valuable insights validated across 4 replication runs with different parameter configurations. Key findings include:

- **Fatigue life is inversely proportional to damage rate** — doubling the per-cycle damage halves the beam's lifespan
- **Fatigue life is directly proportional to material threshold** — stronger materials survive proportionally more cycles
- **Spatial vulnerability follows structural mechanics** — the midspan segment, with the highest damage factor, always fails first under the default configuration
- **The cumulative nature of fatigue is clearly demonstrated** — each individual cycle causes negligible damage, but the accumulation over hundreds of cycles leads to the fatigue limit being reached
- **All 4 replication runs match the theoretical formula exactly** — validating that the simulation correctly implements Miner's Rule
- **A structure reaches its fatigue limit when its most critical section does** — even though the edges are at 50%, the overall bridge is no longer safe because the center (its weakest link) has been fully consumed

The interactive features — including the Tkinter settings GUI for parameter adjustment, the enhanced animated 2D bridge visualization with 5-level color-coded status system, and the retry/close dialog for multi-run comparison — make this tool an effective educational resource for understanding modeling and simulation concepts. The simulation enables users to experiment with different scenarios and observe their effects immediately, reinforcing the value of simulation as a decision-support tool.

---

## Appendix A: File Structure

```
Bridge Simulation/
├── simulation.py                    # Complete simulation: settings GUI + engine + animated 2D + saved charts + retry dialog
├── generate_flowchart.py            # Generates a professional 2D flowchart image for the simulation
├── results/                         # Output folder for generated images
│   ├── damage_distribution.png      # Bar chart of final damage per segment
│   ├── damage_over_time.png         # Line plot of damage growth over cycles
│   └── simulation_flowchart.png     # Generated flowchart of simulation logic
├── DEFENSE_100_PERCENT.md           # 100% defense documentation with replication runs & analysis
├── DEFENSE_75_PERCENT.md            # Original 75% defense document
├── PROJECT_DOCUMENTATION.md         # This file
├── MODEL_DESIGN_DOCUMENTATION.md    # Detailed model design documentation
├── PROPOSAL_DEFENSE_DOCUMENT.md     # Full defense proposal
├── DEFENSE_DELIVERY_SCRIPT.md       # Slide-by-slide speaking guide
├── DEFENSE_CHEAT_SHEET.md           # Printable one-page reference
├── POWERPOINT_SLIDES.md             # PowerPoint slide content guide
└── .gitignore                       # Git ignore rules
```

## Appendix B: How to Run

```bash
# Install dependencies
pip install numpy matplotlib

# Run the simulation
python simulation.py
```

### Steps:
1. **Settings GUI opens** — adjust parameters using sliders and text fields
2. Click **"Run Simulation"** to start (or **"Reset Defaults"** to restore defaults)
3. Console prints cycle-by-cycle damage progress (every 50 cycles)
4. **Enhanced animated 2D bridge window opens** — watch damage grow in real time
5. Close the animation window → **Result images saved to `results/`**
6. **Retry/Close dialog appears** — view summary and choose to retry or exit

### System Requirements

| Resource | Requirement |
|----------|-------------|
| Python | 3.8+ (tested with 3.14.0) |
| NumPy | 1.20+ (tested with 2.4.2) |
| Matplotlib | 3.5+ (tested with 3.10.8) |
| Tkinter | Built-in with Python (no install needed) |
| Hardware | Any modern PC |
| Execution time | < 5 seconds per run |

---

*This is a conceptual simulation for educational purposes in Modeling & Simulation. It demonstrates fatigue principles using a normalized damage accumulation model and is not intended for real-world structural analysis.*
