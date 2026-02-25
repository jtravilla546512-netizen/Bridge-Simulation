# A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

## Project Documentation (Normalized / Conceptual Model)

---

## 1. Introduction

Modeling and Simulation is a computational technique used to represent and analyze real-world systems without the need for costly physical experiments. It is particularly valuable in structural engineering, where physical testing of full-scale structures such as bridges is impractical and expensive. By creating computational models of structural behavior, we can predict how components respond to various loading conditions over time.

Structural fatigue — the progressive weakening of a material subjected to repeated (cyclic) loading — is one of the leading causes of bridge failures. Even when individual load cycles are well below the material's strength, the cumulative effect of many loading cycles can eventually lead to failure.

This project focuses on developing a **Python-based conceptual simulation** of structural fatigue in bridge beams under repeated loading. The simulation uses a **normalized damage accumulation model** to demonstrate the core principles of fatigue. It models a bridge beam divided into 3 segments, applies cyclic damage based on position-dependent factors, tracks damage accumulation at each segment, and presents results through **animated 2D visualization and 3D modeling**.

### Core Formula

| Formula | Meaning |
|---------|---------|
| `damage += damage_increment * segment_factor` | Damage grows each cycle based on position |
| `If damage >= failure_threshold -> FAILURE` | When accumulated damage reaches 1.0, the segment fails |

### Simulation Entities

| Entity | Description |
|--------|-------------|
| **Bridge Beam** | The primary structural element being simulated |
| **Beam Segments** | 3 portions of the beam where damage is tracked individually |
| **Load Cycles** | Repeated loading events applied to the beam |
| **Fatigue Damage State** | The condition (0.0 to 1.0) of each beam segment |

---

## 2. Problem Description

Bridge beams are subjected to repeated loading from vehicular traffic throughout their operational life. Each load cycle, while individually harmless, contributes incrementally to fatigue damage within the structural material. Over time, this accumulated damage can lead to structural failure.

The key problems motivating this study include:

- **Fatigue is invisible in early stages.** Damage accumulates gradually and cannot be seen until it's too late.
- **Physical testing is impractical.** Full-scale fatigue testing is expensive and time-consuming, making simulation the preferred approach.
- **Predictive capability is needed.** Engineers need to estimate remaining fatigue life to plan maintenance.
- **Position-dependent vulnerability.** Different parts of the beam experience different damage rates — the center is most vulnerable.

A simulation approach allows us to model damage accumulation, predict failure, and visualize the progressive degradation process — all conceptually and computationally.

---

## 3. Research Objectives

This simulation framework aims to:

1. **Evaluate the fatigue life of a bridge beam** under repeated loading and determine how many cycles it can sustain before structural failure occurs
2. **Identify the relationship between damage increment and cycles to failure** — specifically, how increasing the damage rate affects the beam's lifespan
3. **Analyze the spatial distribution of fatigue damage** — determine which beam segments are most vulnerable based on their position (center vs. edges)
4. **Visualize the progressive degradation process** — provide animated 2D and 3D representations of how a healthy beam transitions through safe, warning, critical, and failed states over time
5. **Demonstrate the cumulative nature of fatigue** — show that individually harmless load cycles can accumulate to cause structural failure
6. **Enable parameter manipulation** — allow users to change damage increment, failure threshold, and segment factors to observe how different conditions affect fatigue behavior
7. **Determine the sensitivity of fatigue life to input parameters** — evaluate which parameters have the greatest influence on how long the beam survives

Ultimately, the goal is to **understand and demonstrate how cumulative fatigue damage leads to structural failure** and to provide visual, interactive evidence of the factors that accelerate or delay that failure.

---

## 4. Methodology / Approach

### 4.1 Conceptual Model Design

The simulation is built around four core entities:

1. **Bridge Beam** — A simply-supported structural element divided into segments.
2. **Beam Segments** — The beam is divided into 3 segments (left, center, right), each tracking its own damage state.
3. **Load Cycles** — Repeated loading events that continue until failure is detected.
4. **Fatigue Damage State** — Each segment has a damage value from 0.0 (new) to 1.0+ (failed).

### 4.2 Damage Accumulation

```
damage += damage_increment * segment_factor
```

- **damage_increment**: Fixed normalized value per cycle (default: 0.002)
- **segment_factor**: Position-based multiplier:
  - Segment 1 (left): 0.5 — near support, lower vulnerability
  - Segment 2 (center): 1.0 — at midspan, highest vulnerability
  - Segment 3 (right): 0.5 — near support, lower vulnerability

### 4.3 Failure Detection

```
If damage >= failure_threshold -> Segment has FAILED
```

Default threshold: 1.0

### 4.4 Status Classification

| Damage Ratio | Status | Visual Color |
|-------------|--------|-------------|
| 0% - 25% | SAFE | Green |
| 25% - 50% | LOW DAMAGE | Yellow |
| 50% - 75% | WARNING | Orange |
| 75% - 100%+ | CRITICAL / FAILED | Red |

### 4.5 Simulation Flow

1. Set parameters (damage_increment, failure_threshold, segment_factors)
2. Initialize 3 beam segments with damage = 0.0
3. **Loop** through each cycle:
   - `damage += damage_increment * segment_factor` for each segment
   - Check if `damage >= failure_threshold`
   - Record state for visualization
4. Display animated 2D visualization
5. Display 3D beam model
6. Save result charts to `results/` folder

---

## 5. Input Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `damage_increment` | Damage added per cycle (normalized, 0 to 1) | 0.002 |
| `failure_threshold` | When damage reaches this value, segment fails | 1.0 |
| `num_segments` | Number of beam divisions | 3 |
| `segment_factors` | Position-based damage multipliers | [0.5, 1.0, 0.5] |
| `animation_speed` | Milliseconds between animation frames | 20 |
| `cycles_per_frame` | How many cycles to advance per frame | 2 |

---

## 6. Output Variables

| Output | Description |
|--------|-------------|
| Animated 2D visualization | Real-time beam with colored segments, damage gauge, status, chart |
| 3D beam model | Final-state beam with colored segments and crack effects |
| Damage distribution | Bar chart of final damage per segment (saved as PNG) |
| Damage over time | Line plot of damage growth across cycles (saved as PNG) |
| Console summary | Cycle-by-cycle text output with final statistics |
| Cycles to failure | Exact cycle number when first segment reaches threshold |
| Maximum damage | Highest damage value reached by any segment |
| Beam status | Overall status: SAFE, WARNING, or FAILED |

---

## 7. Assumptions

1. The beam is simply-supported (supported at both ends)
2. Load is applied repeatedly at the center of the beam
3. Damage accumulation is linear: `D += damage_increment * factor`
4. Failure occurs at `D >= 1.0` — a normalized conceptual threshold
5. Position-dependent vulnerability is modeled through segment factors
6. All segments are independent — damage in one does not affect neighbors
7. Environmental factors (temperature, corrosion, humidity) are not considered
8. The beam geometry remains unchanged throughout the simulation
9. Damage is irreversible — it can only increase, never decrease
10. This is a **conceptual model** for educational purposes, not for real-world structural analysis

---

## 8. Flowchart

The simulation follows this logical flow:

```
START
  |
Set Parameters (damage_increment, threshold, factors)
  |
Initialize 3 Beam Segments (damage = 0.0 each)
  |
+--------------- LOOP ----------------+
|  For each segment:                  |
|  damage += damage_increment * factor|
|  |                                  |
|  Damage >= threshold?               |
|  |YES --> FAILURE DETECTED --> EXIT  |
|  |NO --> Loop Back (next cycle)     |
+-----------+-------------------------+
            |
   Animated 2D Visualization
            |
   3D Beam Model (Final State)
            |
   Save Results (PNG images)
            |
   Print Console Summary
            |
           END
```

---

## 9. Simulation Results

### Default Parameters
- Mode: Run until failure (no max_cycles limit)
- damage_increment: 0.002
- failure_threshold: 1.0
- segment_factors: [0.5, 1.0, 0.5]

### Results

| Segment | Position | Factor | Final Damage | Percentage | Status |
|---------|----------|--------|-------------|-----------|--------|
| Segment 1 | Left | 0.5 | 0.500 | 50% | WARNING |
| Segment 2 | Center | 1.0 | 1.000 | 100% | **FAILED** |
| Segment 3 | Right | 0.5 | 0.500 | 50% | WARNING |

- **Failure occurs at cycle 500** — Segment 2 (center) reaches threshold
- **Edge segments at 50%** at the same point — half the factor, half the damage
- **Key insight:** Center segment is most vulnerable due to position factor of 1.0

### Parameter Sensitivity

| Change | Effect |
|--------|--------|
| Double `damage_increment` (0.004) | Center fails at cycle **250** instead of 500 |
| Triple `damage_increment` (0.006) | Center fails at cycle **167** |
| Raise `failure_threshold` to 2.0 | Center fails at cycle **1000** |
| Equal factors [1.0, 1.0, 1.0] | All segments fail at same cycle |
| Higher center factor [0.3, 1.5, 0.3] | Center fails faster, edges slower |

---

## 10. Feasibility Assessment

### 10.1 Technical Feasibility — FEASIBLE

- **Python ecosystem** provides all necessary tools: NumPy for computation, Matplotlib for animation and 3D visualization
- **Normalized model** is straightforward to implement and computationally lightweight
- Simulation runs successfully with animated output plus saved images
- Execution time: under 5 seconds

### 10.2 Educational Feasibility — FEASIBLE

- The conceptual model clearly demonstrates fatigue damage principles
- Simulated results match expected physical behavior:
  - Center of beam is most vulnerable (highest factor)
  - Damage accumulates linearly and predictably
  - Failure occurs when threshold is reached
- Entities are well-defined and map to simulation modeling concepts
- Animation makes the invisible process of fatigue visible

### 10.3 Resource Requirements — MINIMAL

| Resource | Requirement |
|----------|-------------|
| Python | 3.8+ |
| NumPy | 1.20+ |
| Matplotlib | 3.5+ |
| Hardware | Any modern PC |
| Time | < 5 seconds to run |

### 10.4 Limitations

1. Uses normalized conceptual model — not certified engineering calculations
2. No explicit stress or force computations
3. No environmental factors (temperature, corrosion)
4. Segments are independent (no neighbor interaction)
5. Single uniform loading pattern (fixed damage increment)
6. Not suitable for real-world structural safety decisions

### 10.5 Potential Problems and Mitigations

| Problem | Mitigation |
|---------|-----------|
| Damage accumulates too fast/slow | Adjust damage_increment parameter |
| Want different segment counts | Change num_segments and segment_factors |
| Animation too fast/slow | Adjust animation_speed and cycles_per_frame |
| Want to test different scenarios | Change parameters at top of file, re-run |
| No real units system | Intentional — this is a normalized conceptual model |

---

## 11. File Structure

```
Bridge Simulation/
+-- simulation.py                # Complete simulation: logic + animated 2D + 3D + saved charts
+-- results/                     # Output folder for generated images
|   +-- damage_distribution.png  # Bar chart of final damage per segment
|   +-- damage_over_time.png     # Line plot of damage growth over cycles
+-- PROJECT_DOCUMENTATION.md     # This file
+-- PROPOSAL_DEFENSE_DOCUMENT.md # Full defense proposal
+-- DEFENSE_DELIVERY_SCRIPT.md   # Slide-by-slide speaking guide
+-- DEFENSE_CHEAT_SHEET.md       # Printable one-page reference
```

---

## 12. How to Run

```bash
# Install dependencies
pip install numpy matplotlib

# Run the simulation
python simulation.py
```

### What Happens:
1. Console prints cycle-by-cycle damage progress
2. **Animated 2D window opens** — watch damage grow in real-time
3. Close the animation window -> **3D beam view appears**
4. Close the 3D window -> **Result images saved to results/**
5. Final summary printed to console

### To Change Parameters:
Open `simulation.py` and edit the values at the top of the file:
```python
damage_increment = 0.002   # Damage per cycle
failure_threshold = 1.0    # When to fail
segment_factors = [0.5, 1.0, 0.5]  # Position multipliers
```

---

*This is a conceptual simulation for educational purposes in Modeling & Simulation. It demonstrates fatigue principles using a normalized damage accumulation model and is not intended for real-world structural analysis.*
