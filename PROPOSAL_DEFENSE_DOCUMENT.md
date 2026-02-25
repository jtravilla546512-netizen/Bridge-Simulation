# Proposal Defense Document

## A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

### Modeling & Simulation

---

## 1. Background of the Problem

Bridges are continuously subjected to repeated loads such as vehicles, pedestrians, and environmental forces. Although these loads may not cause immediate failure, their repeated application over time can lead to structural fatigue, particularly in critical components like bridge beams. Fatigue damage accumulates gradually and may eventually result in cracking, reduced strength, or structural failure if not properly monitored. In real-world engineering, predicting fatigue life often requires extensive material data, long-term monitoring, and complex calculations, which are not always feasible for academic or conceptual studies.

To address this challenge, this study proposes a simulation-based approach that will focus on visualizing and analyzing how fatigue damage accumulates in a bridge beam under repeated loading. Instead of relying on exact material properties or real-world measurements, the simulation will use a normalized damage model to represent fatigue progression. This approach will allow students and researchers to clearly observe trends in damage accumulation, identify critical regions of the beam, and understand failure behavior in a controlled environment.

The study will be centered on a simplified bridge beam divided into three segments, where repeated loads will be applied over a series of cycles. Each cycle will represent one instance of loading, and damage will accumulate incrementally in each segment. By simulating this process, the study will demonstrate how fatigue develops over time and which areas of the beam are most vulnerable.

---

## 2. Purpose of the Simulation

The main aim of the simulation is to study how fatigue damage accumulates in a bridge beam under repeated loading conditions. Specifically, the simulation will seek to:

- Visualize the progression of fatigue damage over load cycles
- Compare damage accumulation across different beam segments
- Identify the point at which structural failure occurs
- Demonstrate the concept of fatigue life in a clear and intuitive way

This simulation is intended to serve as a conceptual and educational tool, rather than a precise engineering design calculator.

### 2.1 Goals and Objectives

The following are the formal goals and objectives of this simulation project:

**Goal:** To develop a Python-based simulation that will model and visualize how cumulative fatigue damage leads to structural failure in a bridge beam under repeated cyclic loading.

**Objectives:**

1. **Simulate cumulative fatigue damage** — Implement a cycle-based damage accumulation model where each load cycle will incrementally increase the damage state of each beam segment.
2. **Model position-dependent vulnerability** — Use segment factors to represent the structural principle that the midspan of a simply-supported beam experiences higher bending stress than the supports.
3. **Detect and report structural failure** — The simulation will automatically identify when any beam segment reaches the failure threshold and report the exact cycle at which failure occurs.
4. **Provide real-time animated visualization** — Create an animated 2D display that will show color-coded beam segments, a damage gauge, beam status indicator, and live damage chart that updates every cycle.
5. **Generate 3D visual output** — Render a 3D beam model that will show the final damage distribution across all segments.
6. **Enable parameter experimentation** — Allow users to manipulate simulation parameters (damage increment, failure threshold, segment factors) to explore different fatigue scenarios and observe cause-effect relationships.

---

## 2.2 Simulation Entities

In simulation modeling, an **entity** is any object or component that is created, processed, and tracked throughout the simulation. The following entities will be defined in this simulation:

| Entity | Type | Description |
|--------|------|-------------|
| **Bridge Beam** | Primary Entity | The main structural object to be simulated; will be composed of 3 segments |
| **Beam Segment** | Sub-Entity | An individual portion of the beam (Left, Center, Right) that will have its own damage state, position factor, and status |
| **Load Cycle** | Event Entity | One application of repeated load to the beam; the simulation will process one cycle per iteration |
| **Fatigue Damage State** | State Entity | The current damage condition of each segment, ranging from 0.0 (undamaged) to 1.0 (failed) |

### Entity Lifecycle

1. The **Bridge Beam** entity will be **created** at the start of the simulation with 3 sub-entities (segments).
2. Each **Beam Segment** will be **assigned** initial attributes: damage = 0.0, factor = [0.5, 1.0, 0.5], status = SAFE.
3. A **Load Cycle** event will be generated for each iteration until failure is detected.
4. During each cycle, the **Fatigue Damage State** will be updated (processed) for every segment.
5. When a segment's damage reaches the threshold, it will be **disposed** (marked as FAILED and removed from active processing).

---

## 2.3 Simulation Variables

Variables will define the inputs, outputs, and internal state of the simulation. They are categorized into three types:

### Input Variables (User-Defined Parameters)

| Variable | Symbol | Type | Default | Description |
|----------|--------|------|---------|-------------|
| Damage Increment | `damage_increment` | Float | 0.002 | Normalized damage added per cycle per unit factor |
| Failure Threshold | `failure_threshold` | Float | 1.0 | Damage level at which a segment will be declared failed |
| Number of Segments | `num_segments` | Integer | 3 | How many divisions the beam will be split into |
| Segment Factors | `segment_factors` | List[Float] | [0.5, 1.0, 0.5] | Position-based damage multipliers for each segment |

### State Variables (Will Change During Simulation)

| Variable | Symbol | Type | Range | Description |
|----------|--------|------|-------|-------------|
| Current Cycle | `cycle` | Integer | 1 to failure | The current iteration number |
| Segment Damage | `damage[i]` | Float | 0.0 to 1.0 | Accumulated fatigue damage for segment i |
| Segment Status | `status[i]` | String | SAFE/WARNING/FAILED | Current condition of segment i |
| Beam Status | `beam_status` | String | SAFE/WARNING/FAILED | Overall beam condition (worst segment) |

### Output Variables (Expected Results)

| Variable | Description |
|----------|-------------|
| Final Damage per Segment | The damage value of each segment at simulation end |
| Maximum Damage | The highest damage value among all segments |
| Cycles to Failure | The cycle number at which the first segment will reach the threshold |
| Damage History | Complete time-series array of damage values per segment per cycle |
| Saved Charts | damage_distribution.png and damage_over_time.png |

---

## 3. Visual Representation / Floor Plan of the Simulation

The simulation will use a top-down and side-view conceptual model of a bridge beam. The beam will be visually represented as a horizontal structure supported at both ends and divided into three segments: left, center, and right. A repeated downward load will be applied at the center of the beam to represent traffic or dynamic loading.

Color changes will be used to indicate the level of fatigue damage in each segment:

| Damage Level | Color | Status |
|-------------|-------|--------|
| 0% - 25% | Green | SAFE |
| 25% - 50% | Yellow | LOW DAMAGE |
| 50% - 75% | Orange | WARNING |
| 75% - 100% | Red | CRITICAL / FAILED |

The planned visual elements will include:
- **Fatigue Damage Gauge** — A vertical bar indicator that will show the maximum damage percentage
- **Beam Status Indicator** — Will display the overall beam condition (SAFE, WARNING, or FAILED)
- **Cycle Counter** — Will show the current load cycle number and simulation parameters
- **Damage Chart** — A real-time line graph that will show damage accumulation over cycles

This visual layout will allow users to easily understand the process flow of the simulation and observe how damage evolves spatially and temporally.

---

## 3.1 Model Design and Structure (Process Flow)

In simulation modeling, entities move through a structured process consisting of **Create, Assign, Decide, Process, and Dispose** steps. The following table maps each step to the corresponding action that will be implemented in this simulation:

| Process Step | Simulation Action | Description |
|-------------|-------------------|-------------|
| **CREATE** | Initialize Beam Segments | Three beam segment entities will be created at the start. Each segment will represent a portion of the bridge beam (Left, Center, Right). |
| **ASSIGN** | Set Initial Attributes | Each segment will be assigned: damage = 0.0, segment_factor = [0.5, 1.0, 0.5], status = "SAFE". Global parameters (damage_increment, failure_threshold) will also be assigned. |
| **DECIDE** | Check Failure Condition | After each cycle, the simulation will check: Is `damage[i] >= failure_threshold`? If YES → mark as FAILED and proceed to DISPOSE. If NO → loop back to PROCESS for the next cycle. |
| **PROCESS** | Accumulate Damage | During each cycle, damage will be processed: `damage[i] += damage_increment * segment_factor[i]`. This will be the core computation that changes the state of each entity. |
| **DISPOSE** | Mark Failed / End Simulation | When a segment reaches the failure threshold, it will be disposed (marked as FAILED and no longer accumulates damage). The simulation will then end and produce output. |

### Process Flow Diagram (Create → Assign → Decide → Process → Dispose)

```
[CREATE]                    [ASSIGN]                     [PROCESS]
Initialize 3 Beam    -->   Set damage=0,          -->   For each cycle:
Segments (entities)        factors=[0.5,1.0,0.5]        damage += increment * factor
                           status="SAFE"
                                                              |
                                                              v
                                                         [DECIDE]
                                                         damage >= threshold?
                                                        /              \
                                                      YES               NO
                                                       |                |
                                                  [DISPOSE]         Loop back
                                                  Mark FAILED       to PROCESS
                                                  End simulation    (next cycle)
                                                  Generate outputs
```

This mapping demonstrates that the proposed simulation will follow a complete and logical model structure consistent with simulation modeling principles.

---

## 4. How the Simulation Model Will Work

The simulation will operate on a cycle-based logic. Each cycle will represent one repeated application of load to the bridge beam. During every cycle, a small amount of fatigue damage will be added to each beam segment. The amount of damage added will depend on predefined segment factors, where the center segment will experience higher damage due to greater bending effects.

### Core Formula

```
damage += damage_increment * segment_factor
```

### Segment Factors

| Segment | Position | Factor | Reason |
|---------|----------|--------|--------|
| Segment 1 | Left (near support) | 0.5 | Lower bending stress near supports |
| Segment 2 | Center (midspan) | 1.0 | Highest bending stress at midspan |
| Segment 3 | Right (near support) | 0.5 | Lower bending stress near supports |

### Failure Condition

```
If damage >= failure_threshold (1.0) --> Segment has FAILED
```

The simulation will continue iterating through cycles until the damage in any beam segment reaches the failure threshold. There is no maximum cycle limit — the simulation will run continuously until failure is detected.

All damage values will be recorded throughout the simulation to enable visualization and post-simulation analysis.

### Manipulable Parameters

Users will be able to modify the following parameters at the top of the simulation file to experiment with different conditions:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `damage_increment` | Damage added per cycle (normalized, 0 to 1) | 0.002 |
| `failure_threshold` | Damage level at which failure occurs | 1.0 |
| `num_segments` | Number of beam divisions | 3 |
| `segment_factors` | Position-based damage multipliers | [0.5, 1.0, 0.5] |

---

## 5. Expected Behavior of the Bridge Beam Under Repeated Loading

Under repeated loading, the beam will not move physically in the simulation but will instead degrade structurally. With each load cycle, internal fatigue damage will increase, especially in the middle segment where bending stresses are typically highest in real bridges.

As cycles progress, damage is expected to accumulate faster in critical regions, eventually reaching a point where the beam will be considered structurally failed. This behavior reflects real-world fatigue mechanisms, where failure is the result of gradual degradation rather than sudden collapse.

### Expected Damage Progression (Default Parameters)

Based on the mathematical model (`damage = damage_increment × segment_factor × cycle`), the expected damage values are:

| Cycle | Segment 1 | Segment 2 | Segment 3 | Beam Status |
|-------|-----------|-----------|-----------|-------------|
| 1 | 0.001 | 0.002 | 0.001 | SAFE |
| 100 | 0.100 | 0.200 | 0.100 | SAFE |
| 250 | 0.250 | 0.500 | 0.250 | WARNING |
| 400 | 0.400 | 0.800 | 0.400 | CRITICAL |
| 500 | 0.500 | 1.000 | 0.500 | FAILED |

---

## 6. What the Simulation Will Measure

The simulation will measure normalized fatigue damage for each beam segment over time. Damage values will range from 0 (no damage) to 1 (failure). The primary measured outputs will include:

| Measurement | Description |
|-------------|-------------|
| **Fatigue damage per segment** | Individual damage level of each of the 3 segments |
| **Maximum damage across the beam** | The highest damage value among all segments |
| **Number of cycles until failure** | How many load cycles before the first segment fails |
| **Damage progression trends** | How damage grows over time (linear accumulation) |

These measurements will allow comparison between segments and provide insight into structural vulnerability.

### Expected Results and Preliminary Analysis

Based on the mathematical model and default parameters, the following results are expected:

1. **Linear damage accumulation** — Damage is expected to increase at a constant rate per cycle, consistent with Miner's Rule of linear cumulative damage. The center segment should gain 0.002 damage per cycle; edge segments should gain 0.001 per cycle.

2. **Position-dependent failure** — The center segment (factor 1.0) is expected to always fail first, reaching 100% damage at cycle 500. Edge segments (factor 0.5) should reach only 50% damage at the same point. This will confirm that the model correctly represents midspan vulnerability.

3. **Inverse relationship between increment and fatigue life** — Doubling the damage increment from 0.002 to 0.004 is expected to reduce cycles to failure from 500 to 250. This inverse proportionality (`cycles_to_failure = threshold / (increment × factor)`) is mathematically predictable and will be verified by the simulation.

4. **Threshold sensitivity** — Raising the failure threshold from 1.0 to 2.0 should double the fatigue life to 1000 cycles, demonstrating that the threshold directly controls how much damage the beam can absorb before failure.

5. **No segment interaction** — Each segment will accumulate damage independently. There will be no load redistribution when one segment degrades, which is a simplification that could be addressed in future versions.

These expected outcomes indicate that the simulation should produce valid, analyzable, and predictable outputs that align with established fatigue theory.

### Planned Output Files

| Output | Type | Description |
|--------|------|-------------|
| Animated 2D visualization | Interactive | Real-time beam with colored segments, gauge, status, chart |
| 3D beam model | Interactive | Final-state beam showing damage distribution in 3D |
| damage_distribution.png | Saved image | Bar chart of final damage per segment |
| damage_over_time.png | Saved image | Line plot of damage accumulation over cycles |

---

## 7. Significance and Expected Outcomes of the Simulation

This simulation will help achieve a better understanding of structural fatigue behavior without requiring complex material data or real-world experiments. It will demonstrate how repeated loading affects structural components over time and highlight the importance of monitoring fatigue in critical infrastructure.

### Expected Outcomes
- The center segment (factor 1.0) is expected to reach failure first, while edge segments (factor 0.5) will accumulate half the damage
- With default parameters, the center segment should fail at cycle 500 and the edge segments should be at 50% damage
- Doubling the damage increment should halve the cycles to failure
- Increasing the failure threshold should allow the beam to survive more cycles

### Significance
- Can be used as a **teaching tool** for demonstrating fatigue concepts in Modeling & Simulation courses
- Will serve as a **conceptual study model** for understanding cumulative damage behavior
- Will provide a **foundation for advanced simulations** involving real material properties and load data
- Will offer **clear animated visualization** that makes the invisible process of fatigue damage visible and intuitive

Ultimately, the simulation is expected to provide a clear visualization of fatigue progression and support informed discussions on structural safety, maintenance planning, and failure prevention.

---

## 8. Simulation Flowchart

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
|  |YES --> FAILURE DETECTED --> EXIT |
|  |NO                                |
|  Loop Back (next cycle)             |
+------------+------------------------+
             |
   Display Animated 2D Visualization
             |
   Display 3D Beam Model
             |
   Save Result Charts (PNG)
             |
   Print Console Summary
             |
            END
```

---

## 9. Definition of Terms

| Term | Definition |
|------|-----------|
| **Structural Fatigue** | Progressive weakening of a structure under repeated cyclic loading |
| **Damage Increment** | The fixed amount of damage added per cycle (normalized value) |
| **Failure Threshold** | The damage level at which a segment is considered failed (default: 1.0) |
| **Segment Factor** | Position-based multiplier that controls how fast each segment degrades |
| **Damage Index (D)** | Cumulative measure from 0.0 (undamaged) to 1.0 (failed) |
| **Load Cycle** | One application of repeated load, representing one vehicle crossing event |
| **Beam Segment** | A portion of the beam where damage is tracked individually |
| **Simply-Supported Beam** | A beam supported at both ends, loaded from above |
| **Cycles to Failure** | Number of load cycles until damage reaches the failure threshold |
| **Cumulative Damage** | Total accumulated damage from all past load cycles (irreversible) |
| **Normalized Model** | A model using values scaled from 0 to 1 instead of real engineering units |

---

## 10. References

1. Miner, M. A. (1945). "Cumulative Damage in Fatigue." *Journal of Applied Mechanics*, 12(3), A159-A164.
2. Palmgren, A. (1924). "Die Lebensdauer von Kugellagern." *Zeitschrift des Vereins Deutscher Ingenieure*, 68, 339-341.
3. Dowling, N. E. (2012). *Mechanical Behavior of Materials*. 4th Ed., Pearson.
4. Banks, J. et al. (2010). *Discrete-Event System Simulation*. 5th Ed., Pearson.
5. Law, A. M. (2015). *Simulation Modeling and Analysis*. 5th Ed., McGraw-Hill.
6. Harris, C. R. et al. (2020). "Array programming with NumPy." *Nature*, 585, 357-362.
7. Hunter, J. D. (2007). "Matplotlib: A 2D graphics environment." *Computing in Science & Engineering*, 9(3), 90-95.
8. Schijve, J. (2009). *Fatigue of Structures and Materials*. 2nd Ed., Springer.
9. Suresh, S. (1998). *Fatigue of Materials*. 2nd Ed., Cambridge University Press.
10. ACI Committee 215 (1997). *Considerations for Design of Concrete Structures Subjected to Fatigue Loading*. American Concrete Institute.

---

*This proposal presents a conceptual simulation design for educational purposes in Modeling & Simulation. It will use a normalized damage accumulation model to demonstrate fatigue principles and is not intended for certified structural analysis.*
