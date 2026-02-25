# Model Design Documentation

## A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

---

## What is Model Design?

Model Design explains **how the system is represented in the simulation software**. In ARENA (Rockwell), you drag modules from a panel and connect them visually. In Python, we write code that performs the **exact same logic** — just in text instead of a visual flowchart.

The key idea is the same: **entities are created, given attributes, processed through logic, checked by decisions, and eventually disposed**.

---

## How ARENA Modules Map to Python Code

In ARENA, you use visual modules. In our Python simulation, each module is represented by a specific block of code inside `simulation.py`. The logic is identical — only the tool is different.

### Module Mapping Table

| ARENA Module | Python Equivalent | What It Does in Our Simulation | Code Location |
|-------------|-------------------|-------------------------------|---------------|
| **Create** | Initialization block | Generates 3 beam segment entities at the start | Lines 110-114 |
| **Assign** | Parameter assignment | Sets damage=0, factors=[0.5,1.0,0.5], status="SAFE" | Lines 34-42, 110-114 |
| **Process** | While loop body | Accumulates damage: `damage += increment * factor` | Lines 117-119 |
| **Decide** | If-statement check | Checks: `damage >= threshold?` → YES=fail, NO=loop | Lines 127-132 |
| **Dispose** | Break + output | Marks segment FAILED, stops loop, generates results | Lines 134, 443-491 |
| **Record** | History arrays | Stores every cycle's data for charts and analysis | Lines 121-124 |

---

## Detailed Module Breakdown

### 1. CREATE Module — Initialize Beam Segments

**ARENA equivalent:** A Create module that generates entities (e.g., "Customer arrives every X minutes").

**Our simulation:** At the start, 3 beam segment entities are created. Each one represents a portion of the bridge beam.

```python
# CREATE — Initialize beam segment entities
beam_segments = [0.0] * num_segments   # 3 segments, all starting at 0 damage
```

| Property | Value |
|----------|-------|
| Number of entities created | 3 (left, center, right) |
| Entity type | Beam Segment |
| Creation time | Once, at simulation start |
| Initial state | damage = 0.0 for all |

**ARENA comparison:** In ARENA, you would use a Create module set to "1 entity at time 0" and then use a Separate or Batch to create 3 copies. In Python, we simply create a list of 3 values.

---

### 2. ASSIGN Module — Set Initial Attributes

**ARENA equivalent:** An Assign module that sets attribute values on entities (e.g., "Set Service Time = EXPO(5)").

**Our simulation:** Each segment is assigned its initial attributes — damage value, segment factor, and status.

```python
# ASSIGN — Set parameters for each segment
damage_increment = 0.002               # Damage added per cycle
failure_threshold = 1.0                 # When to fail
segment_factors = [0.5, 1.0, 0.5]      # Position-based multipliers

# Each segment gets:
# - damage = 0.0 (from beam_segments initialization)
# - factor = segment_factors[i]
# - status = "SAFE" (derived from damage = 0)
```

| Attribute | Segment 1 (Left) | Segment 2 (Center) | Segment 3 (Right) |
|-----------|------------------|--------------------|--------------------|
| damage | 0.0 | 0.0 | 0.0 |
| factor | 0.5 | 1.0 | 0.5 |
| status | SAFE | SAFE | SAFE |

**ARENA comparison:** In ARENA, you would drag an Assign module after Create and set `Attribute "Factor" = 0.5`. In Python, we assign these values directly.

---

### 3. PROCESS Module — Accumulate Damage (Core Logic)

**ARENA equivalent:** A Process module where entities seize a resource, experience a delay (service), and release the resource.

**Our simulation:** During each load cycle, every beam segment is "processed" — it receives damage based on its position factor. This is the core computation.

```python
# PROCESS — Accumulate damage each cycle
while True:
    cycle += 1
    for i in range(num_segments):
        beam_segments[i] += damage_increment * segment_factors[i]
```

| Process Detail | Description |
|---------------|-------------|
| Formula | `damage[i] += damage_increment * segment_factor[i]` |
| Frequency | Once per cycle, for each segment |
| Center segment | Gets 0.002 damage per cycle (factor 1.0) |
| Edge segments | Get 0.001 damage per cycle (factor 0.5) |
| Equivalent in ARENA | Process module with "Delay" = damage accumulation time |

**ARENA comparison:** In ARENA, a Process module would "Seize-Delay-Release" a resource. In our simulation, each cycle is like one "service event" where the beam absorbs one unit of loading stress. The `damage_increment * factor` is conceptually similar to a processing delay — it represents the work (damage) done during that cycle.

---

### 4. DECIDE Module — Check Failure Condition

**ARENA equivalent:** A Decide module with a condition (e.g., "If Queue Length > 5, go to True, else False").

**Our simulation:** After processing each cycle, the simulation checks whether any segment has reached the failure threshold.

```python
# DECIDE — Check if damage >= threshold
for i in range(num_segments):
    if beam_segments[i] >= failure_threshold:
        failure_cycle = cycle           # YES → record failure
        break                           # → proceed to DISPOSE
# If no failure → loop back to PROCESS (next cycle)
```

| Decision | Condition | TRUE Path | FALSE Path |
|----------|-----------|-----------|------------|
| Failure check | `damage[i] >= 1.0` | Go to DISPOSE (end) | Loop back to PROCESS |

**How it works:**

```
                    +------------------+
                    | damage >= 1.0 ?  |
                    +------------------+
                      /            \
                    YES             NO
                     |              |
              [DISPOSE]      [Loop back to
              End sim         PROCESS for
              Mark FAILED     next cycle]
```

**ARENA comparison:** In ARENA, you would place a Decide module with type "2-way by Condition" and set the condition to `Attribute "Damage" >= 1.0`. The True exit goes to Dispose; the False exit loops back to Process.

---

### 5. DISPOSE Module — Mark Failed and End

**ARENA equivalent:** A Dispose module that removes entities from the system (e.g., "Customer leaves the store").

**Our simulation:** When a segment reaches the failure threshold, it is "disposed" — marked as FAILED. The simulation stops and generates all output.

```python
# DISPOSE — When failure is detected
if failure_cycle is not None:
    break   # Exit the simulation loop

# Then generate outputs:
# → Animated 2D visualization
# → 3D beam model
# → Save damage_distribution.png
# → Save damage_over_time.png
# → Print console summary
```

| Dispose Action | Description |
|---------------|-------------|
| Mark as FAILED | Segment status changes to "FAILED" |
| Stop simulation | `break` exits the while loop |
| Generate outputs | Charts, animation, 3D model, summary |
| Equivalent in ARENA | Dispose module + ReadWrite + output statistics |

**ARENA comparison:** In ARENA, the Dispose module removes the entity. In our simulation, `break` ends the loop. The output generation (charts, images) is equivalent to ARENA's Output module or exporting statistics after a run.

---

### 6. RECORD Module — Store Data for Analysis

**ARENA equivalent:** A Record module that tallies statistics or records time intervals.

**Our simulation:** Every cycle, we record the damage values into history arrays for later visualization.

```python
# RECORD — Store cycle data
history_cycles.append(cycle)
for i in range(num_segments):
    history_damages[i].append(beam_segments[i])
history_max_damage.append(max(beam_segments))
```

| What is Recorded | Purpose |
|-----------------|---------|
| Cycle number | X-axis for time plots |
| Damage per segment | Y-axis for damage-over-time chart |
| Maximum damage | Gauge display and failure detection |

**ARENA comparison:** In ARENA, you would use a Record module set to "Count" or "Time Interval" to track statistics. In Python, we append to lists and use those lists to generate matplotlib charts.

---

## Complete Entity Flow

The entity flow follows this sequence, just like entities moving through ARENA modules:

```
[CREATE]          [ASSIGN]          [PROCESS]         [DECIDE]         [DISPOSE]
   |                 |                  |                 |                 |
Generate 3    →   Set damage=0   →   Add damage    →   Damage ≥ 1.0? →  Mark FAILED
beam segment      Set factors        each cycle         |       |        Stop loop
entities          Set status                           YES      NO       Generate
                  ="SAFE"                               |       |        outputs
                                                   [DISPOSE]  [LOOP]
                                                   End sim    Back to
                                                              PROCESS
```

### Entity Lifecycle (from creation to disposal)

| Step | ARENA Module | Python Code | What Happens |
|------|-------------|-------------|--------------|
| 1 | Create | `beam_segments = [0.0] * 3` | 3 segment entities are born |
| 2 | Assign | `segment_factors = [0.5, 1.0, 0.5]` | Attributes are set |
| 3 | Process | `damage += increment * factor` | Damage accumulates each cycle |
| 4 | Decide | `if damage >= threshold` | Check for failure |
| 5a | (NO) | `continue` | Loop back to step 3 |
| 5b | (YES) Dispose | `break` | Entity is "disposed" (failed), simulation ends |

---

## Visual Comparison: ARENA vs Python

### If this were built in ARENA:

```
+----------+    +----------+    +-----------+    +----------+    +-----------+
|  CREATE  | →  |  ASSIGN  | →  |  PROCESS  | →  |  DECIDE  | →  |  DISPOSE  |
| Generate |    | damage=0 |    | damage += |    | damage   |    | Mark      |
| 3 beam   |    | factor=  |    | increment |    | >= 1.0?  |    | FAILED    |
| segments |    | [0.5,    |    | * factor  |    |          |    | End sim   |
|          |    |  1.0,    |    |           |    | NO→back  |    | Output    |
|          |    |  0.5]    |    |           |    | to PROC  |    | results   |
+----------+    +----------+    +-----------+    +----------+    +-----------+
```

### In our Python code (`simulation.py`):

```python
# ┌─────────── CREATE ───────────┐
beam_segments = [0.0] * num_segments

# ┌─────────── ASSIGN ───────────┐
damage_increment = 0.002
failure_threshold = 1.0
segment_factors = [0.5, 1.0, 0.5]

# ┌─────────── SIMULATION LOOP ───────────┐
cycle = 0
while True:
    cycle += 1

    # ┌─────── PROCESS ───────┐
    for i in range(num_segments):
        beam_segments[i] += damage_increment * segment_factors[i]

    # ┌─────── DECIDE ────────┐
    for i in range(num_segments):
        if beam_segments[i] >= failure_threshold:
            failure_cycle = cycle
            break

    # ┌─────── DISPOSE ───────┐
    if failure_cycle is not None:
        break    # End simulation, generate outputs
```

---

## Key Differences: ARENA vs Python

| Aspect | ARENA (Rockwell) | Python (Our Simulation) |
|--------|-----------------|------------------------|
| Interface | Visual drag-and-drop modules | Written code in a .py file |
| Entity creation | Create module on canvas | `beam_segments = [0.0] * 3` |
| Attribute assignment | Assign module dialog box | Variable assignment in code |
| Processing logic | Process module with delay | `damage += increment * factor` |
| Decision making | Decide module with condition | `if damage >= threshold` |
| Entity removal | Dispose module | `break` statement ends loop |
| Data recording | Record module / statistics | Appending to lists, saving PNGs |
| Visualization | ARENA's built-in animation | Matplotlib 2D animation + 3D plot |
| Running | Click "Go" in ARENA | `python simulation.py` in terminal |
| Output | ARENA reports and charts | Console output + saved PNG images |

---

## Why Python Instead of ARENA?

| Reason | Explanation |
|--------|-------------|
| **Custom visualization** | ARENA cannot produce our specific animated beam with color-coded segments, damage gauge, and live chart |
| **Full control** | Python allows us to define the exact damage formula and visual layout |
| **3D modeling** | ARENA does not natively support 3D beam visualization |
| **Accessibility** | Python is free and open-source; ARENA requires a license |
| **Educational value** | Writing the logic in code demonstrates deeper understanding of the simulation process |
| **Same concepts** | The simulation still follows Create → Assign → Process → Decide → Dispose — the same structure ARENA uses |

---

## Summary

Even though this simulation is built in Python instead of ARENA, it follows the **exact same simulation modeling structure**:

1. **Entities are CREATED** — 3 beam segments initialized at the start
2. **Attributes are ASSIGNED** — damage=0, factors, status="SAFE"
3. **Entities are PROCESSED** — damage accumulates each cycle using `damage += increment * factor`
4. **DECISIONS are made** — is `damage >= threshold`? YES → dispose, NO → loop back
5. **Entities are DISPOSED** — failed segment is marked, simulation ends, results are generated

The only difference is the tool: instead of dragging modules on ARENA's canvas, we write the equivalent logic in Python code. The fundamental simulation principles — entity lifecycle, state changes, decision branching, and data collection — are identical.

---

*This document maps ARENA/Rockwell simulation concepts to the Python implementation used in this project. The simulation follows standard Create-Assign-Process-Decide-Dispose methodology.*
