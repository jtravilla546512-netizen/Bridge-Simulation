# PowerPoint Slide Text

## A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

### Modeling & Simulation

---

**Instructions:** Put ONLY these short sentences/bullets on your slides. Everything else goes in your speaking script.

---

## SLIDE 1: Title Slide

- **Title:** A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading
- **Course:** Modeling & Simulation
- **Name:** [Your Name]
- **Date:** February 18, 2026

---

## SLIDE 2: Background of the Problem

- Bridges experience repeated loads from traffic and environmental forces
- Individual loads are harmless, but repeated application causes fatigue
- Fatigue damage accumulates gradually and is invisible in early stages
- Real-world fatigue testing is expensive and impractical for academic study
- This proposal uses a normalized damage model to visualize fatigue progression

---

## SLIDE 3: Goals and Objectives

**Goal:** Develop a Python-based simulation that will model and visualize cumulative fatigue damage in a bridge beam under repeated cyclic loading.

**Objectives:**
1. Simulate cumulative fatigue damage using a cycle-based model
2. Model position-dependent vulnerability using segment factors
3. Detect and report structural failure at the threshold
4. Provide real-time animated 2D visualization
5. Generate a 3D beam model of final damage state
6. Enable parameter experimentation for different fatigue scenarios

---

## SLIDE 4: Simulation Entities

| Entity | Type | Description |
|--------|------|-------------|
| Bridge Beam | Primary Entity | Main structure composed of 3 segments |
| Beam Segment | Sub-Entity | Left, Center, Right — each with own damage state |
| Load Cycle | Event Entity | One application of load per iteration |
| Fatigue Damage State | State Entity | Damage level per segment (0.0 to 1.0) |

---

## SLIDE 5: Simulation Variables

**Input Variables:**
- `damage_increment` = 0.002 | `failure_threshold` = 1.0
- `segment_factors` = [0.5, 1.0, 0.5] | `num_segments` = 3

**State Variables (will change during simulation):**
- `cycle` — current iteration | `damage[i]` — accumulated damage per segment
- `status[i]` — SAFE / WARNING / FAILED

**Output Variables (expected results):**
- Final damage per segment | Maximum damage | Cycles to failure
- Damage history array | Saved charts (PNG)

---

## SLIDE 6: Model Design — Create, Assign, Decide, Process, Dispose

| Step | Action |
|------|--------|
| **CREATE** | Initialize 3 beam segment entities |
| **ASSIGN** | Set damage=0, factors=[0.5, 1.0, 0.5], status=SAFE |
| **DECIDE** | Is damage >= threshold? More cycles remaining? |
| **PROCESS** | `damage += damage_increment × segment_factor` |
| **DISPOSE** | Mark failed segments; end simulation; produce outputs |

```
CREATE → ASSIGN → [LOOP: PROCESS → DECIDE] → DISPOSE
```

---

## SLIDE 7: Visual Representation / Floor Plan

- *(Insert planned layout diagram here)*
- Beam will be divided into 3 segments: Left, Center, Right
- Supported at both ends; load applied at center
- Color will indicate damage: Green (Safe) → Yellow → Orange → Red (Failed)
- Planned visual elements: Damage Gauge, Beam Status, Cycle Counter, Damage Chart

---

## SLIDE 8: How the Simulation Will Work

- Cycle-based logic: each cycle = one load application
- **Formula:** `damage += damage_increment × segment_factor`
- **Failure:** `If damage >= 1.0 → FAILED`
- Center segment: factor = 1.0 (most vulnerable)
- Edge segments: factor = 0.5 (less vulnerable)
- Simulation will run continuously until a segment reaches failure threshold

---

## SLIDE 9: Expected Beam Behavior Under Repeated Loading

- Beam will degrade structurally, not physically
- Center segment expected to accumulate damage fastest
- Damage will be irreversible — only increases

| Cycle | Seg 1 | Seg 2 | Seg 3 | Expected Status |
|-------|-------|-------|-------|-----------------|
| 100 | 10% | 20% | 10% | SAFE |
| 250 | 25% | 50% | 25% | WARNING |
| 500 | 50% | 100% | 50% | FAILED |

---

## SLIDE 10: What the Simulation Will Measure & Expected Analysis

- Fatigue damage per beam segment (0 to 1)
- Maximum damage across the beam
- Number of cycles until failure
- Damage progression trends over time

**Expected Results:**
- Center expected to fail first (factor 1.0); edges at 50%
- Doubling increment should halve fatigue life (500 → 250 cycles)
- Linear damage accumulation expected (consistent with Miner's Rule)
- Planned output: Animated 2D, 3D beam model, saved charts

---

## SLIDE 11: Simulation Flowchart

```
Set Parameters → Initialize Segments → Loop:
  Accumulate Damage → Check Threshold → Not Failed? Loop Back
→ Failure Detected → Generate Visualizations → Save Results → END
```

- *(Insert flowchart image or diagram here)*

---

## SLIDE 12: Significance & Expected Outcomes

- Center segment expected to fail first (factor 1.0); edges at 50% damage
- Doubling damage increment → expected to halve cycles to failure
- Will make invisible fatigue process visible through animation
- Will serve as teaching tool for Modeling & Simulation concepts
- Will provide foundation for more advanced simulations

---

## SLIDE 13: Conclusion

- Fatigue = cumulative damage from repeated loads
- Proposed simulation will use normalized model: `damage += increment × factor`
- Animated visualization will show progressive degradation
- Parameters will be manipulable for experimentation
- Conceptual model for educational purposes

**"Thank you. I'm ready for your questions."**
