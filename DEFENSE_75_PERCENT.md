# 75% DEFENSE DOCUMENTATION
## A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

**Course:** Modeling & Simulation  
**Proponent:** [Your Name]  
**Date:** March 3, 2026  
**Completion:** 75% — Working Simulation with GUI, Animated Visualization, and Results Output

---

# TABLE OF CONTENTS

1. [Problem Definition & Objectives (15%)](#1-problem-definition--objectives-15)
2. [Model Design & Structure (20%)](#2-model-design--structure-20)
3. [Simulation Setup & Execution (15%)](#3-simulation-setup--execution-15)
4. [Data Usage & Analysis (15%)](#4-data-usage--analysis-15)
5. [Presentation & Usability (10%)](#5-presentation--usability-10)
6. [Parameter Explanation Guide](#6-parameter-explanation-guide)
7. [Scope and Limitations](#7-scope-and-limitations)
8. [PowerPoint Slides with Speaking Script](#8-powerpoint-slides-with-speaking-script)

---

---

# 1. PROBLEM DEFINITION & OBJECTIVES (15%)

## 1.1 Problem Statement

Bridges carry thousands of vehicles every single day. Each vehicle that passes creates a small force on the bridge. One car alone does not damage the bridge. But when thousands and thousands of cars pass over the bridge every day, for many years, the small forces add up. This is called **fatigue**.

Fatigue is dangerous because you cannot see it. The bridge looks fine on the outside, but inside, tiny cracks are slowly growing. The damage accumulates silently over time. This has happened in real life — bridges have experienced severe structural fatigue that was not detected until it was too late.

**Important:** This simulation does **not** predict whether a bridge will collapse or break. Instead, it **visualizes how structural fatigue accumulates over time** under repeated loading. It shows the progression of damage — not the moment of collapse.

Testing fatigue on a real bridge is very expensive and takes many years. That is why we built a **computer simulation** — a program that models how fatigue damage accumulates, so we can study the process safely, quickly, and for free.

**The core problem:** How does repeated loading cause cumulative structural fatigue in a bridge beam, and how can we visualize the progression of that damage over time?

## 1.2 Objectives

**Main Goal:** Develop a Python-based simulation that models and visualizes cumulative fatigue damage in a bridge beam under repeated cyclic loading.

**Specific Objectives:**

| # | Objective | Status at 75% |
|---|-----------|---------------|
| 1 | Simulate cumulative fatigue damage using a cycle-based model | ✅ Complete |
| 2 | Model position-dependent vulnerability using segment factors | ✅ Complete |
| 3 | Detect and report structural failure when threshold is reached | ✅ Complete |
| 4 | Provide real-time animated 2D visualization of the bridge | ✅ Complete |
| 5 | Enable parameter experimentation via a GUI settings window | ✅ Complete |
| 6 | Generate and save result charts (damage distribution & damage over time) | ✅ Complete |

All 6 objectives are **fully implemented and working** at the 75% mark.

---

---

# 2. MODEL DESIGN & STRUCTURE (20%)

## 2.1 Simulation Entities

| Entity | Type | Description |
|--------|------|-------------|
| **Bridge Beam** | Primary Entity | The main structure, divided into 3 segments |
| **Beam Segment** | Sub-Entity | Left, Center, and Right — each has its own damage level |
| **Load Cycle** | Event Entity | One application of traffic load per iteration |
| **Fatigue Damage State** | State Entity | Damage level per segment, from 0.0 (no damage) to 1.0 (full fatigue capacity reached) |

## 2.2 Model Flow — Create, Assign, Decide, Process, Dispose

Our simulation follows the standard simulation modeling pattern:

### CREATE
- Initialize 3 beam segment entities (Left, Center, Right)
- Create the GUI settings window for parameter input
- Set up data storage arrays for recording history

### ASSIGN
- Set initial damage of every segment to `0.0` (brand new, no damage)
- Assign damage factors: `[0.5, 1.0, 0.5]` — center gets most damage
- Set status of all segments to `SAFE`
- Load user-configured parameters from the GUI

### DECIDE (checked every cycle)
- **Has damage reached the failure threshold?** → If YES → go to DISPOSE
- **Is damage still below threshold?** → If YES → continue to PROCESS
- **Additional status checks:** SAFE (< 25%), LOW DAMAGE (25-50%), WARNING (50-75%), CRITICAL (75-99%), THRESHOLD REACHED (≥ 100%)

### PROCESS (the main simulation loop)
- Apply the fatigue formula: `damage += damage_increment × segment_factor`
- Record the new damage values into history arrays
- Update cycle counter
- Print console output every 50 cycles

### DISPOSE
- Mark the segment that reached the failure threshold
- Stop the simulation loop
- Generate animated 2D visualization of the entire damage history
- Save result charts (damage distribution bar chart, damage over time line chart)
- Display summary and show Retry/Close dialog

### Flow Diagram

```
┌─────────┐    ┌──────────┐    ┌──────────────────────┐
│  CREATE  │───▶│  ASSIGN  │───▶│   PROCESS (Loop)     │
│ segments │    │ damage=0 │    │ damage += inc × fac  │
│ + GUI    │    │ factors  │    │ record history       │
└─────────┘    └──────────┘    └──────────┬───────────┘
                                          │
                                    ┌─────▼─────┐
                                    │   DECIDE   │
                                    │ damage ≥   │
                                    │ threshold? │
                                    └──┬─────┬──┘
                                  NO   │     │  YES
                                 ┌─────┘     └─────┐
                                 │                  │
                           ┌─────▼───┐        ┌────▼────┐
                           │  LOOP   │        │ DISPOSE │
                           │  BACK   │        │ results │
                           └─────────┘        │ charts  │
                                              │ dialog  │
                                              └─────────┘
```

## 2.3 Color Status System

| Damage Level | Color | Status Label |
|-------------|-------|-------------|
| 0% – 24% | 🟢 Green | SAFE |
| 25% – 49% | 🟡 Yellow | LOW DAMAGE |
| 50% – 74% | 🟠 Orange | WARNING |
| 75% – 99% | 🔴 Red | CRITICAL |
| 100% | 🔴 Dark Red | THRESHOLD REACHED |

---

---

# 3. SIMULATION SETUP & EXECUTION (15%)

## 3.1 How to Run the Simulation

1. **Run the program:** `python simulation.py`
2. **Settings GUI appears** — adjust parameters or keep defaults
3. **Click "Run Simulation"** — simulation runs all cycles instantly
4. **Animated 2D visualization opens** — watch the bridge degrade in real-time
5. **Close the visualization** — results are saved as PNG images
6. **Retry/Close dialog appears** — choose to run again with new parameters or exit

## 3.2 Default Parameters and Their Values

| Parameter | Default Value | What It Controls |
|-----------|--------------|-----------------|
| `damage_increment` | 0.002 | How much damage is added per cycle |
| `failure_threshold` | 1.0 | The damage level representing full fatigue capacity |
| `animation_speed` | 20 ms | How fast the animation plays (milliseconds per frame) |
| `cycles_per_frame` | 2 | How many simulation cycles are shown per animation frame |
| `segment_factors` | [0.5, 1.0, 0.5] | How vulnerable each segment is (Left, Center, Right) |
| `num_segments` | 3 (fixed) | Number of beam segments (Left, Center, Right) |

## 3.3 The Simulation Formula

```
damage += damage_increment × segment_factor
```

Each cycle, every segment gets damaged. The amount of damage depends on:
- **damage_increment** — the base damage per cycle (same for all segments)
- **segment_factor** — a multiplier that makes some segments weaker than others

**If damage ≥ failure_threshold → that segment has reached full fatigue capacity → simulation stops.**

## 3.4 Execution Results (Default Parameters)

With default settings (`damage_increment = 0.002`, `failure_threshold = 1.0`, `factors = [0.5, 1.0, 0.5]`):

| Cycle | Segment 1 (Left) | Segment 2 (Center) | Segment 3 (Right) | Overall Status |
|-------|------------------|--------------------|--------------------|----------------|
| 1 | 0.001 (0%) | 0.002 (0%) | 0.001 (0%) | SAFE |
| 100 | 0.100 (10%) | 0.200 (20%) | 0.100 (10%) | SAFE |
| 250 | 0.250 (25%) | 0.500 (50%) | 0.250 (25%) | WARNING |
| 400 | 0.400 (40%) | 0.800 (80%) | 0.400 (40%) | CRITICAL |
| 500 | 0.500 (50%) | **1.000 (100%)** | 0.500 (50%) | **THRESHOLD REACHED** |

**Result:** Center segment reaches the failure threshold at exactly **cycle 500**. Left and Right segments are at 50% accumulated fatigue.

## 3.5 Output Files Generated

| File | Description |
|------|-------------|
| `results/damage_distribution.png` | Bar chart showing final damage of each segment |
| `results/damage_over_time.png` | Line chart showing damage progression over all cycles |

---

---

# 4. DATA USAGE & ANALYSIS (15%)

## 4.1 Input Data

The simulation uses **user-configurable input parameters** entered through the GUI:

- **damage_increment = 0.002** → Each cycle adds 0.2% of the failure threshold as base damage
- **failure_threshold = 1.0** → Represents 100% of the structural fatigue capacity; at 1.0, the segment has accumulated maximum fatigue
- **segment_factors = [0.5, 1.0, 0.5]** → Center segment accumulates fatigue twice as fast as the edges

These are **normalized values** — they do not represent real-world units (like Pascals or Newtons). They represent *proportions* of total structural capacity.

## 4.2 Data Recorded During Simulation

Every cycle, the simulation records:

| Data Array | What It Stores | Used For |
|-----------|---------------|----------|
| `history_cycles` | Cycle number (1, 2, 3, ..., 500) | X-axis of damage chart |
| `history_damages[i]` | Damage of segment i at each cycle | Line chart & color animation |
| `history_max_damage` | Maximum damage across all segments at each cycle | Gauge indicator |
| `failure_cycle` | The cycle number when failure occurred | Summary report |

## 4.3 Output Analysis

### Finding 1: Center Segment Reaches Threshold First
The center segment (factor = 1.0) accumulates fatigue **twice as fast** as the left and right segments (factor = 0.5). This matches real-world bridge behavior — the center of a beam experiences the highest bending stress under load.

### Finding 2: Damage is Linear
With a constant `damage_increment`, the damage grows in a straight line. This is consistent with **Miner's Rule** of cumulative fatigue damage, which says each load cycle contributes an equal fraction of damage.

### Finding 3: Changing Parameters Changes the Outcome
| Experiment | damage_increment | Expected Cycles to Failure |
|-----------|-----------------|---------------------------|
| Default | 0.002 | 500 cycles |
| Double damage | 0.004 | 250 cycles |
| Half damage | 0.001 | 1000 cycles |
| Higher threshold | 0.002, threshold=2.0 | 1000 cycles |

**Conclusion:** Doubling the damage increment halves the fatigue life. Doubling the threshold doubles the fatigue life. The relationship is **inversely proportional**.

### Finding 4: Position Matters
Segments with higher factors reach the threshold earlier. If we change factors to `[1.0, 1.0, 1.0]`, all segments reach the threshold at the same time. If we change to `[0.2, 1.0, 0.8]`, the center still reaches the threshold first, but the right segment is close behind.

## 4.4 Preliminary Conclusions

1. **Fatigue accumulation is predictable** — with known parameters, we can calculate exactly when the threshold will be reached
2. **Location matters** — segments under more stress (higher factor) accumulate fatigue sooner
3. **Small damages add up** — even 0.002 per cycle eventually reaches the threshold after 500 cycles
4. **The simulation correctly models Miner's Rule** — linear cumulative damage under constant amplitude loading

**Important note:** These conclusions describe how fatigue *accumulates* — the simulation does not predict structural collapse or failure mode. It visualizes the *process* of fatigue buildup over time.

---

---

# 5. PRESENTATION & USABILITY (10%)

## 5.1 GUI Settings Window

The simulation starts with a **Tkinter-based settings window** that allows users to change all parameters without editing any code:

- **Text fields** for damage increment, failure threshold, animation speed, cycles per frame
- **Sliders** for damage increment and failure threshold for quick adjustment
- **Segment factor inputs** for Left, Center, and Right segments
- **Run Simulation button** — starts the simulation with current settings
- **Reset Defaults button** — restores all parameters to original values
- **Window is centered on screen** for clean presentation

## 5.2 Animated 2D Bridge Visualization

The main visualization includes:

| Component | Location | What It Shows |
|-----------|----------|--------------|
| **Bridge Model** | Top (large) | Enhanced bridge with piers, deck, railings, water, road markings, vehicle icon |
| **Damage Gauge** | Middle-left | Vertical bar showing max damage % with color fill |
| **Status Indicator** | Middle-center-left | Overall beam status (SAFE/WARNING/CRITICAL/THRESHOLD REACHED) with color |
| **Info Panel** | Middle-center-right | Current cycle number and parameter summary |
| **Segment Details** | Middle-right | Individual damage % and status for each segment |
| **Damage Chart** | Bottom (wide) | Real-time line chart of damage over cycles |

The bridge segments **change color in real-time** from green to yellow to orange to red as damage increases.

## 5.3 Retry/Close Feature

After the simulation completes:
- A **summary dialog** appears showing all results
- **Retry button** — returns to the settings GUI to run again with different parameters
- **Close button** — exits the program
- This allows **experimentation** — users can test different scenarios without restarting

## 5.4 All Windows Centered on Screen

Every window in the application (Settings GUI, Matplotlib visualization, Retry dialog) is automatically **centered on the user's screen** for a professional and clean appearance.

---

---

# 6. PARAMETER EXPLANATION GUIDE

This section explains **every parameter** in the simulation — what it is, what it does, and how changing it affects the results.

---

### 6.1 `damage_increment` — Damage Per Cycle

| Property | Value |
|----------|-------|
| **Default** | 0.002 |
| **Range** | 0.0005 to 0.05 (adjustable via slider) |
| **Type** | Float (decimal number) |

**What is it?**  
This is the **base amount of damage** that gets added to each segment every single cycle. Think of it like this: every time a truck drives over the bridge, it causes a tiny scratch. The `damage_increment` is how big that scratch is.

**How does it affect the simulation?**
- **Higher value (e.g., 0.004)** → More damage per cycle → Threshold reached sooner → Fewer cycles
- **Lower value (e.g., 0.001)** → Less damage per cycle → Bridge lasts longer → More cycles to failure
- **Relationship:** Cycles to failure = `failure_threshold / (damage_increment × max_factor)`
- With default values: `1.0 / (0.002 × 1.0) = 500 cycles`

**Real-world meaning:** A higher damage_increment represents heavier traffic (bigger trucks, more weight) or weaker bridge materials.

---

### 6.2 `failure_threshold` — Fatigue Capacity Limit

| Property | Value |
|----------|-------|
| **Default** | 1.0 |
| **Range** | 0.1 to 5.0 (adjustable via slider) |
| **Type** | Float (decimal number) |

**What is it?**  
This is the **maximum fatigue a segment can accumulate** before the simulation considers it fully fatigued. Think of it as the bridge's total fatigue capacity. When damage reaches this number, that segment has reached its limit and the simulation stops.

**How does it affect the simulation?**
- **Higher value (e.g., 2.0)** → More fatigue can accumulate before the threshold is reached → More cycles
- **Lower value (e.g., 0.5)** → Threshold is reached sooner → Fewer cycles
- The value 1.0 represents **100% of structural fatigue capacity** — a normalized scale

**Real-world meaning:** A higher threshold represents a bridge with greater fatigue endurance (stronger materials, better design). A lower threshold represents a bridge with less fatigue resistance.

---

### 6.3 `animation_speed` — Visual Speed

| Property | Value |
|----------|-------|
| **Default** | 20 ms |
| **Range** | Any positive integer |
| **Type** | Integer (whole number, in milliseconds) |

**What is it?**  
This controls **how fast the animation plays**. It is the time delay between each animation frame, measured in milliseconds (1 second = 1000 milliseconds).

**How does it affect the simulation?**
- **Lower value (e.g., 5 ms)** → Animation plays faster → Harder to see details
- **Higher value (e.g., 100 ms)** → Animation plays slower → Easier to observe each step
- **This does NOT affect the simulation results** — only how fast you see them

**Real-world meaning:** This is just a display setting. The simulation math is the same regardless of animation speed.

---

### 6.4 `cycles_per_frame` — Data Points Per Frame

| Property | Value |
|----------|-------|
| **Default** | 2 |
| **Range** | Any positive integer |
| **Type** | Integer (whole number) |

**What is it?**  
This controls **how many simulation cycles are shown in each animation frame**. If set to 2, the animation skips every other cycle to make the animation shorter.

**How does it affect the simulation?**
- **Lower value (e.g., 1)** → Every single cycle is shown → Animation is longer, more detailed
- **Higher value (e.g., 10)** → Animation skips many cycles → Animation is shorter, less smooth
- **This does NOT affect the simulation results** — only how the animation is displayed

**Real-world meaning:** This is like fast-forward on a video. The results are the same, you just see them faster.

---

### 6.5 `segment_factors` — Vulnerability Multipliers

| Property | Value |
|----------|-------|
| **Default** | [0.5, 1.0, 0.5] |
| **Range** | 0.1 to 2.0 per segment |
| **Type** | List of 3 floats |

**What is it?**  
Each segment has a **damage factor** that multiplies the base `damage_increment`. This makes some parts of the bridge weaker or stronger than others.

| Segment | Position | Default Factor | Meaning |
|---------|----------|----------------|---------|
| Segment 1 | Left | 0.5 | Gets **half** the base damage per cycle |
| Segment 2 | Center | 1.0 | Gets the **full** base damage per cycle |
| Segment 3 | Right | 0.5 | Gets **half** the base damage per cycle |

**How does it affect the simulation?**
- Center factor is highest (1.0) → Center always reaches the threshold first with default settings
- If you set all factors to 1.0 → All segments take equal damage → All reach the threshold at the same time
- If you set Left to 2.0 → Left segment gets **double** the base damage → Left reaches the threshold first

**Real-world meaning:** In a real bridge, the center of a beam bends the most under load — that is why the center has the highest factor. The ends are supported by piers and experience less stress.

**The formula per segment per cycle:**
```
damage_for_segment_i = damage_increment × segment_factor[i]
```
Example for center segment: `0.002 × 1.0 = 0.002 damage per cycle`  
Example for left segment: `0.002 × 0.5 = 0.001 damage per cycle`

---

### 6.6 `num_segments` — Number of Bridge Parts

| Property | Value |
|----------|-------|
| **Default** | 3 (fixed) |
| **Type** | Integer |

**What is it?**  
The bridge beam is divided into **3 fixed segments**: Left, Center, and Right. This cannot be changed in the GUI.

**Why 3 segments?**  
A simply supported beam (supported at both ends) has a natural stress pattern with 3 zones: low stress at the left support, high stress at the center, and low stress at the right support. Three segments model this pattern simply and clearly.

---

---

# 6B. ACADEMIC JUSTIFICATION OF DEFAULT PARAMETERS

This section provides the engineering reasoning behind each default parameter value, so you can explain **why** these specific numbers were chosen if asked during the defense.

---

## Why `segment_factors = [0.5, 1.0, 0.5]`?

**Source:** Simply-supported beam bending moment distribution (fundamental structural mechanics).

When a uniform load acts on a simply-supported beam (a beam resting on two supports at its ends), the **bending moment** — the internal force that causes stress — follows a parabolic distribution:

```
Moment distribution along a simply-supported beam:

  Support                Center                Support
    |                      |                      |
    |        ___M_max___   |                      |
    |      /             \ |                      |
    |    /                 \                      |
    |  /                     \                    |
    |/                         \                  |
    +---------------------------+
    0        L/4    L/2    3L/4         L
```

- **Maximum bending moment** occurs at the center: $M_{max} = \frac{wL^2}{8}$
- **Zero bending moment** at the supports (the two ends)
- The moment at the quarter-points (roughly where our left/right segments are) is approximately **half** of the maximum

Since fatigue damage is proportional to stress, and stress is proportional to bending moment:
- **Center segment factor = 1.0** → experiences the maximum bending stress (normalized)
- **Left and Right segment factors = 0.5** → experience approximately half the bending stress

This is a simplified but physically meaningful representation of how stress varies along a real bridge beam. The 0.5 : 1.0 : 0.5 ratio captures the essential pattern that **the center of a beam is the most vulnerable to fatigue**.

**Reference:** Any introductory Mechanics of Materials or Structural Analysis textbook covers simply-supported beam bending moment diagrams (e.g., Hibbeler, *Mechanics of Materials*; Beer & Johnston, *Mechanics of Materials*).

---

## Why `damage_increment = 0.002`?

**Reasoning:** This is a **normalized value** chosen for simulation clarity, not derived from a specific physical measurement.

The value 0.002 was selected because:

1. **Clean cycle count:** With `failure_threshold = 1.0` and `max_factor = 1.0`:
   $$\text{Cycles to threshold} = \frac{1.0}{0.002 \times 1.0} = 500 \text{ cycles}$$
   500 is a round number that is easy to understand and discuss.

2. **Good visualization range:** 500 cycles produces a smooth, watchable animation — enough frames for the user to observe the gradual color transition from green through yellow, orange, to red, but not so many that the animation takes forever.

3. **Represents 0.2% of capacity per cycle:** Each cycle consumes $\frac{0.002}{1.0} \times 100\% = 0.2\%$ of the fatigue capacity. This is a small, incremental amount — consistent with the concept of fatigue where each individual load event causes negligible damage, but the cumulative effect is significant.

4. **Consistent with Miner's Rule normalization:** In Miner's Rule, the damage fraction per cycle is $\frac{1}{N_f}$ where $N_f$ is the number of cycles to reach the threshold. Setting $N_f = 500$ gives $\frac{1}{500} = 0.002$, which is exactly our `damage_increment`.

**Important:** The user can adjust this value via the GUI slider (range: 0.0005 to 0.05) to experiment with different fatigue rates. The default is just a starting point that balances clarity and computational speed.

---

## Why `failure_threshold = 1.0`?

**Reasoning:** 1.0 represents **100% of fatigue capacity** on a normalized 0-to-1 scale.

This is the standard normalization used in Miner's Rule:
$$D = \sum_{i=1}^{k} \frac{n_i}{N_i}$$

Where $D = 1.0$ indicates that the fatigue capacity has been fully consumed. Using 1.0 makes the damage values directly interpretable as percentages (0.5 = 50%, 0.8 = 80%, etc.).

---

---

# 7. SCOPE AND LIMITATIONS

## 7.1 Scope — What the Simulation DOES

1. **Models cumulative fatigue damage** — simulates how damage adds up over many load cycles using a simplified linear model
2. **Divides the bridge into 3 segments** — Left, Center, and Right — each with its own damage factor representing different stress levels
3. **Provides a GUI for parameter input** — users can change all simulation parameters without editing code
4. **Animates the bridge in 2D** — shows real-time color changes, gauges, status indicators, and damage charts as the simulation plays
5. **Detects and reports failure** — automatically stops when any segment reaches the failure threshold
6. **Saves result charts** — generates and saves damage distribution and damage-over-time charts as PNG images
7. **Supports retry/experimentation** — after each run, users can retry with different parameters or close the program
8. **Shows console output** — prints cycle-by-cycle damage values and a final summary to the terminal

## 7.2 Limitations — What the Simulation DOES NOT Do

| # | Limitation | Explanation |
|---|-----------|-------------|
| 1 | **No real-world units** | Damage values are normalized (0.0 to 1.0), not in real engineering units like stress (MPa) or force (kN). This is a conceptual model, not an engineering calculator. |
| 2 | **Linear damage only** | Damage increases at a constant rate every cycle. In real life, fatigue damage can accelerate near failure (non-linear behavior). Our model uses Miner's Rule which assumes linearity. |
| 3 | **Fixed 3 segments** | The bridge is always divided into 3 parts. A real bridge may have hundreds or thousands of elements. This simplification is intentional for visualization clarity. |
| 4 | **No variable loading** | Every load cycle applies the same damage increment. In real life, traffic loads vary — some trucks are heavier than others. Our model assumes constant amplitude loading. |
| 5 | **No repair or recovery** | Once fatigue damage is accumulated, it never decreases. There is no way to simulate bridge repair or maintenance during the simulation. |
| 6 | **No environmental factors** | The simulation does not model wind, temperature changes, earthquakes, corrosion, or other environmental effects that can cause fatigue in real bridges. |
| 7 | **No material properties** | The simulation does not use real material data (steel grade, concrete strength, etc.). The segment factors are abstract multipliers, not physical material properties. |
| 8 | **2D visualization only** | The bridge is shown as a 2D side view. There is no 3D structural analysis or finite element modeling. |
| 9 | **Single beam only** | The simulation models one beam. A real bridge has many beams, cables, connections, and other structural members working together. |
| 10 | **No random variation** | Every run with the same parameters produces the exact same result. There is no randomness or statistical variation, unlike real-world fatigue which has scatter. |

## 7.3 Assumptions

1. Damage accumulates **linearly** — each cycle adds the same amount (Miner's Rule)
2. The bridge beam is **simply supported** — held at both ends
3. Load is applied **at the center** of the beam
4. All load cycles are **identical** in magnitude
5. The simulation stops at a **single threshold** value — this represents fully accumulated fatigue, not structural collapse
6. The 3 segments are **independent** — damage in one segment does not affect the others
7. **The simulation shows fatigue accumulation, not structural collapse** — it does not predict when or how a bridge would physically fail

---

---

# 8. POWERPOINT SLIDES WITH SPEAKING SCRIPT

Below are the slides for the 75% defense, along with a **simple speaking script** for each slide — written to be easy to understand and deliver, like explaining it to someone for the first time.

---

## SLIDE 1: Title Slide

**On the Slide:**
- **Title:** A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading
- **Course:** Modeling & Simulation
- **Name:** [Your Name]
- **Date:** March 3, 2026
- **Completion:** 75%

**Speaking Script:**
> "Good day everyone. My name is [Your Name]. My project is called 'A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading.' This is for our Modeling and Simulation class. Today I am presenting the 75 percent completion of my project. I already have a working simulation with a graphical user interface, animated visualization, and saved results."

---

## SLIDE 2: Background of the Problem

**On the Slide:**
- Bridges experience repeated loads from traffic every day
- Individual loads are small, but they add up over time — this is called fatigue
- Fatigue damage is invisible — you cannot see it until it is too late
- Testing on real bridges is expensive and takes years
- Our solution: a computer simulation to model and visualize fatigue

**Speaking Script:**
> "So what is the problem? Every day, cars and trucks drive over bridges. Each vehicle puts a small force on the bridge. One car alone does not cause noticeable damage. But after thousands and thousands of cars, over many years, the small forces add up. This is called fatigue. The scary thing about fatigue is that you cannot see it. The bridge looks normal on the outside, but inside, tiny cracks are growing. We cannot test this on a real bridge because it is too expensive and takes too long. So I built a computer simulation — a program that models how fatigue accumulates so we can study it safely, quickly, and for free."

---

## SLIDE 3: Goals and Objectives

**On the Slide:**
- **Goal:** Develop a Python-based simulation that models and visualizes cumulative fatigue damage in a bridge beam under repeated loading
- **Objectives (all completed):**
  1. ✅ Simulate cumulative fatigue damage using a cycle-based model
  2. ✅ Model position-dependent vulnerability using segment factors
  3. ✅ Detect when fatigue reaches the threshold and report it
  4. ✅ Provide real-time animated 2D visualization
  5. ✅ Enable parameter experimentation via GUI
  6. ✅ Generate and save result charts

**Speaking Script:**
> "My main goal is to build a Python simulation that shows how fatigue damage builds up in a bridge beam. I have 6 specific objectives. First, simulate damage that adds up every cycle. Second, make different parts of the bridge take different amounts of damage. Third, detect when damage reaches the failure threshold and stop the simulation. Fourth, show it all with a live animated picture of the bridge. Fifth, let the user change the settings using a window with buttons and text boxes, without touching the code. Sixth, save the results as chart images. As of today, all 6 objectives are complete and working."

---

## SLIDE 4: Simulation Entities

**On the Slide:**

| Entity | Type | Description |
|--------|------|-------------|
| Bridge Beam | Primary Entity | Main structure with 3 segments |
| Beam Segment | Sub-Entity | Left, Center, Right — each has own damage |
| Load Cycle | Event Entity | One truck passing = one cycle |
| Fatigue Damage State | State Entity | Damage level from 0.0 to 1.0 |

**Speaking Script:**
> "My simulation has 4 entities. The first is the Bridge Beam — this is the main thing we are simulating. It is divided into 3 parts called segments. The second entity is the Beam Segment — I have 3 of them: Left, Center, and Right. Each one keeps track of its own damage separately. The third entity is the Load Cycle — think of this as one truck driving over the bridge. Every time a truck passes, that is one cycle. The fourth entity is the Fatigue Damage State — this is the damage number for each segment, starting at 0 meaning no damage, and going up to 1.0 which means the fatigue threshold has been reached."

---

## SLIDE 5: Simulation Variables

**On the Slide:**

**Input Variables (user can change):**
| Variable | Default | Meaning |
|----------|---------|---------|
| `damage_increment` | 0.002 | Damage added per cycle |
| `failure_threshold` | 1.0 | Fatigue capacity limit |
| `segment_factors` | [0.5, 1.0, 0.5] | Weakness per segment |
| `animation_speed` | 20 ms | How fast animation plays |
| `cycles_per_frame` | 2 | Cycles shown per frame |

**State Variables (change during simulation):**
- `cycle` — current cycle number
- `damage[i]` — accumulated damage for each segment
- `status[i]` — SAFE / WARNING / CRITICAL / THRESHOLD REACHED

**Output Variables (results):**
- Final damage per segment, cycles to failure, saved PNG charts

**Speaking Script:**
> "The simulation has three types of variables. First, input variables — these are the settings that the user can change. The damage increment is 0.002, which means each cycle adds a tiny bit of damage. The failure threshold is 1.0 — when damage reaches this number, that part of the bridge has accumulated maximum fatigue. The segment factors are 0.5, 1.0, and 0.5, which means the center part gets the most damage. The animation speed is 20 milliseconds per frame — this is just how fast the animation looks. And cycles per frame is 2, which means we skip every other cycle to make the animation shorter. Second, state variables — these change while the simulation is running. The cycle counter goes up by 1 every loop. The damage for each segment goes up a little every cycle. The status changes from SAFE to WARNING to CRITICAL to THRESHOLD REACHED as damage increases. Third, output variables — these are the results. The final damage of each segment, the cycle when the threshold was reached, and the charts that are saved as picture files."

---

## SLIDE 6: Model Design — Create, Assign, Decide, Process, Dispose

**On the Slide:**

| Step | What Happens |
|------|-------------|
| **CREATE** | Initialize 3 beam segments + GUI window |
| **ASSIGN** | Set damage=0, factors=[0.5, 1.0, 0.5], status=SAFE |
| **PROCESS** | `damage += damage_increment × segment_factor` |
| **DECIDE** | Is damage ≥ threshold? If No → loop back. If Yes → stop |
| **DISPOSE** | Mark failure, generate charts, show results, save images |

```
CREATE → ASSIGN → [LOOP: PROCESS → DECIDE] → DISPOSE
```

**Speaking Script:**
> "My simulation follows the standard design pattern we learned in class: Create, Assign, Decide, Process, Dispose. In the Create step, I initialize 3 beam segments and open the settings window. In Assign, I set all damage to zero, set the damage factors, and set the status to SAFE. In Process, I apply the formula — damage equals damage plus damage increment times segment factor. This is the core of the simulation. In Decide, I check: is the damage greater than or equal to the threshold? If no, I go back to Process and do another cycle. If yes, I go to Dispose. In Dispose, I mark which segment reached the threshold, I generate the animated visualization, I save the charts, and I show the summary. Then the user can choose to retry with different settings or close the program."

---

## SLIDE 7: Visual Representation — Bridge Layout

**On the Slide:**
- *(Screenshot of the 2D bridge visualization)*
- Bridge has: piers, road deck, railings, water below, vehicle icon
- 3 beam segments below the deck: Left, Center, Right
- Colors show damage: Green → Yellow → Orange → Red
- Indicators: Damage Gauge, Status, Info Panel, Segment Details, Damage Chart

**Speaking Script:**
> "This is what the simulation looks like when it runs. At the top, you see the bridge. It has concrete piers holding it up, a road on top with dashed lines, railings on the sides, and water underneath. There is even a small red truck on the road to show the load. Below the road deck are the 3 beam segments — Left, Center, and Right. These segments change color as they get damaged. Green means safe, yellow means a little damage, orange means warning, and red means the fatigue is near or at the threshold. Below the bridge, there are 4 small panels: a damage gauge that fills up like a health bar, a status box that says SAFE or WARNING or THRESHOLD REACHED, an info panel showing the current cycle and parameters, and a segment detail panel showing the exact percentage for each segment. At the very bottom, there is a line chart that shows how damage grows over time."

---

## SLIDE 8: How the Simulation Works

**On the Slide:**
- Formula: `damage += damage_increment × segment_factor`
- Failure condition: `If damage ≥ 1.0 → THRESHOLD REACHED`
- Center segment: factor = 1.0 (most vulnerable — gets full damage)
- Edge segments: factor = 0.5 (less vulnerable — gets half damage)
- Runs continuously until the threshold is reached
- With defaults: Center reaches threshold at exactly cycle 500

**Speaking Script:**
> "Let me explain how the math works. It is actually very simple. Every cycle, I use this formula: damage equals damage plus damage increment times segment factor. So if the damage increment is 0.002 and the segment factor is 1.0, then that segment gets 0.002 damage added every cycle. For the center segment, with a factor of 1.0, after 500 cycles the damage is 0.002 times 500, which equals 1.0. And 1.0 is our failure threshold, so the center reaches full fatigue at cycle 500. For the left and right segments, the factor is only 0.5, so they only get 0.001 damage per cycle. After 500 cycles, they are at 0.5, which is only 50 percent. So the center always reaches the threshold first because it has the highest factor. This makes sense in real life too — the middle of a bridge bends the most under heavy trucks."

---

## SLIDE 9: Actual Simulation Results

**On the Slide:**

| Cycle | Seg 1 (Left) | Seg 2 (Center) | Seg 3 (Right) | Status |
|-------|-------------|----------------|---------------|--------|
| 1 | 0.1% | 0.2% | 0.1% | SAFE |
| 100 | 10% | 20% | 10% | SAFE |
| 250 | 25% | 50% | 25% | WARNING |
| 400 | 40% | 80% | 40% | CRITICAL |
| 500 | 50% | **100%** | 50% | **THRESHOLD REACHED** |

**Speaking Script:**
> "Here are the actual results from running my simulation with the default settings. At cycle 1, all segments have almost zero damage — everything is safe. At cycle 100, the center is at 20 percent and the sides are at 10 percent. At cycle 250, the center reaches 50 percent — this is the halfway point, and the status changes to WARNING because the center is now in the orange zone. At cycle 400, the center is at 80 percent — this is CRITICAL. And finally at cycle 500, the center hits 100 percent. It has reached the failure threshold. The simulation stops. The left and right segments are at 50 percent — they have accumulated some fatigue but have not reached the threshold yet. This shows that the center accumulates fatigue fastest because it has the highest factor."

---

## SLIDE 10: Data Analysis and Findings

**On the Slide:**
- **Finding 1:** Center segment always reaches the threshold first (factor 1.0 vs 0.5)
- **Finding 2:** Damage growth is linear (straight line on chart)
- **Finding 3:** Doubling damage_increment → halves fatigue life (500 → 250 cycles)
- **Finding 4:** Doubling failure_threshold → doubles fatigue life (500 → 1000 cycles)
- **Conclusion:** Results match Miner's Rule of linear cumulative damage

**Speaking Script:**
> "From the results, I found 4 important things. Finding 1: The center segment always reaches the threshold first because it has the highest damage factor. This matches real-world bridge behavior. Finding 2: The damage grows in a straight line — it increases by the same amount every cycle. This is called linear damage, and it follows a rule in engineering called Miner's Rule. Finding 3: If I double the damage increment from 0.002 to 0.004, the threshold is reached at 250 cycles instead of 500. That is exactly half. So more damage per cycle means a shorter fatigue life. Finding 4: If I double the failure threshold from 1.0 to 2.0, the bridge lasts 1000 cycles instead of 500. So a higher fatigue capacity means more cycles before the threshold is reached. My conclusion is that the simulation correctly follows Miner's Rule — the damage adds up in a straight line, and we can predict exactly when the threshold will be reached."

---

## SLIDE 11: Simulation Flowchart

**On the Slide:**
```
START → Open Settings GUI → User Sets Parameters → Run Simulation
  → Initialize Segments (damage=0) → Loop:
    → Add Damage (formula) → Check: damage ≥ threshold?
    → NO → Next Cycle (loop back)
    → YES → Stop Loop → Show Animation → Save Charts
  → Show Summary → Retry or Close?
    → Retry → Back to Settings GUI
    → Close → END
```

**Speaking Script:**
> "This is the flowchart of my simulation. It starts by opening the settings window where the user can change the parameters. After clicking Run, the simulation begins. First, it sets all segment damage to zero. Then it enters a loop. Every cycle, it adds damage to each segment using the formula. Then it checks: is any segment's damage greater than or equal to the threshold? If no, it does another cycle. If yes, it stops the loop. Then it shows the animated visualization of the bridge, saves the result charts as images, and prints a summary. After that, a dialog appears asking: do you want to retry with new settings, or close the program? If retry, it goes back to the settings window. If close, the program ends."

---

## SLIDE 12: Features Implemented at 75%

**On the Slide:**
- ✅ Working simulation engine with fatigue formula
- ✅ GUI settings window (Tkinter) — no code editing needed
- ✅ Animated 2D bridge visualization with enhanced design
- ✅ Real-time color-coded damage indicators
- ✅ Damage gauge, status panel, info panel, segment details
- ✅ Damage-over-time line chart
- ✅ Saved result images (PNG)
- ✅ Retry/Close dialog for experimentation
- ✅ All windows centered on screen

**Speaking Script:**
> "At 75 percent, here is everything that is working in my simulation. The simulation engine works — it correctly calculates damage using the formula. The settings window lets the user change all parameters using a nice window with text boxes and sliders. The animated 2D bridge visualization shows a realistic bridge with piers, road, railings, and water. The segments change color in real-time as damage increases. There are 4 indicator panels: a damage gauge, a status indicator, an info panel, and segment details. There is a damage chart at the bottom that draws the lines as the animation plays. After the animation, the charts are saved as PNG images. And there is a retry dialog that lets you go back and try again with different settings. All windows are centered on the screen automatically."

---

## SLIDE 13: Scope and Limitations

**On the Slide:**

**Scope:**
- Simulates linear cumulative fatigue in a 3-segment bridge beam
- User-configurable parameters via GUI
- Real-time 2D animated visualization
- Saved chart outputs

**Limitations:**
- No real-world units (normalized 0 to 1 values)
- Linear damage only (no acceleration near failure)
- Fixed 3 segments, single beam
- No variable loading, no repair, no environmental factors
- No randomness — same input = same output every time

**Speaking Script:**
> "Let me talk about the scope and limitations. The scope of my project is to simulate fatigue damage in a bridge beam divided into 3 segments, with a GUI for changing settings, an animated visualization, and saved results. But there are limitations. First, I do not use real-world units — the numbers are normalized from 0 to 1, not in engineering units like megapascals. Second, the damage is linear — in real life, damage can speed up near the end, but my model adds the same amount every cycle. Third, the bridge is always 3 segments and one beam — a real bridge has many more parts. Fourth, every load cycle is the same — in real life, some trucks are heavier than others. Fifth, there is no repair — damage only goes up, never down. Sixth, there are no weather or earthquake effects. And seventh, there is no randomness — if you use the same settings, you get the same result every time. These limitations are acceptable because this is a conceptual educational model, not a real engineering tool."

---

## SLIDE 14: Conclusion and Next Steps

**On the Slide:**
- Fatigue = cumulative damage from repeated loads
- Simulation formula: `damage += increment × factor`
- Working simulation with GUI, animation, and saved results
- Center segment reaches the threshold first (highest factor)
- Results match Miner's Rule (linear cumulative damage)
- **Next steps for 100%:** Additional analysis, documentation, and refinements

**"Thank you. I'm ready for your questions."**

**Speaking Script:**
> "To wrap up: fatigue is damage that adds up from repeated loads. My simulation uses a simple formula — damage equals damage plus increment times factor — to model this. At 75 percent, I have a fully working simulation with a settings window, animated bridge visualization, and saved charts. The center segment reaches the threshold first because it has the highest factor, and the results match Miner's Rule, which says damage adds up in a straight line. For the remaining 25 percent, I will add more analysis, improve the documentation, and make refinements. That is the end of my presentation. Thank you for listening, and I am ready for your questions."

---

---

# APPENDIX A: Quick Reference — Rubric Alignment

| Rubric Criterion | Weight | What I Demonstrated | Score Target |
|-----------------|--------|--------------------|--------------| 
| **Problem Definition & Objectives** | 15% | Clear problem (fatigue is invisible + dangerous), 6 precise objectives all completed | 15/15 |
| **Model Design & Structure** | 20% | Complete Create→Assign→Decide→Process→Dispose flow, logical 3-segment structure, proper entities | 20/20 |
| **Simulation Setup & Execution** | 15% | Simulation runs correctly, all parameters configurable via GUI, valid outputs generated | 15/15 |
| **Data Usage & Analysis** | 15% | Input data explained, outputs analyzed with 4 findings, preliminary conclusions match Miner's Rule | 15/15 |
| **Presentation & Usability** | 10% | Well-organized slides + script, GUI is easy to use, visual flow is clear with enhanced bridge design | 10/10 |
| **TOTAL** | **75%** | | **75/75** |

---

# APPENDIX B: How to Run the Simulation

```
Step 1: Make sure Python 3 is installed with numpy and matplotlib
Step 2: Open a terminal in the project folder
Step 3: Run: python simulation.py
Step 4: Adjust parameters in the Settings window (or keep defaults)
Step 5: Click "Run Simulation"
Step 6: Watch the animated bridge visualization
Step 7: Close the animation window → results are saved
Step 8: Choose "Retry" to try again or "Close" to exit
```

---

# APPENDIX C: File Structure

```
Bridge Simulation/
├── simulation.py                  ← Main simulation program (850 lines)
├── results/
│   ├── damage_distribution.png    ← Bar chart of final damage
│   ├── damage_over_time.png       ← Line chart of damage progression
│   └── simulation_flowchart.png   ← Flowchart diagram
├── DEFENSE_75_PERCENT.md          ← This document
├── POWERPOINT_SLIDES.md           ← Original slide text
├── MODEL_DESIGN_DOCUMENTATION.md  ← Technical model documentation
├── PROJECT_DOCUMENTATION.md       ← Full project documentation
├── PROPOSAL_DEFENSE_DOCUMENT.md   ← Original proposal defense
├── DEFENSE_CHEAT_SHEET.md         ← Quick reference cheat sheet
├── DEFENSE_DELIVERY_SCRIPT.md     ← Original delivery script
└── generate_flowchart.py          ← Flowchart generator
```
