# DEFENSE CHEAT SHEET — Print This!

## A Python-Based Simulation of Structural Fatigue in Bridge Beams Under Repeated Loading

---

## SLIDE ORDER (Follow This)

| # | Slide | What to Emphasize |
|---|-------|-------------------|
| 1 | Title | State your name and title |
| 2 | Background | Fatigue = cumulative damage from repeated loads |
| 3 | Goals & Objectives | Goal + 6 numbered objectives |
| 4 | Entities | 4 entities: Beam, Segments, Cycles, Damage State |
| 5 | Variables | Input (5 params), State (cycle, damage, status), Output (results) |
| 6 | Model Design | Create → Assign → Decide → Process → Dispose |
| 7 | Visual / Floor Plan | Point to layout: beam, colors, gauge, chart |
| 8 | How It Will Work | Formula + segment factors + failure condition |
| 9 | Expected Beam Behavior | Center expected to fail first, show the table |
| 10 | What It Will Measure + Expected Analysis | Damage per segment, expected conclusions |
| 11 | Flowchart | Loop: accumulate -> check -> repeat |
| 12 | Significance | Teaching tool, will make fatigue visible, foundation |
| 13 | Conclusion | Summary + "ready for questions" |

---

## THE FORMULA

```
damage += damage_increment * segment_factor
If damage >= 1.0 --> FAILED
```

---

## SEGMENT FACTORS

| Segment | Position | Factor | Expected Damage at Cycle 500 |
|---------|----------|--------|------------------------------|
| Seg 1 | Left | 0.5 | 50% (WARNING) |
| Seg 2 | Center | **1.0** | **100% (FAILED)** |
| Seg 3 | Right | 0.5 | 50% (WARNING) |

Center gets DOUBLE the damage --> expected to fail first.

---

## COLOR CODE

| Color | Damage | Status |
|-------|--------|--------|
| Green | 0-25% | SAFE |
| Yellow | 25-50% | LOW DAMAGE |
| Orange | 50-75% | WARNING |
| Red | 75-100% | CRITICAL/FAILED |

---

## PARAMETERS (Will Be Changeable)

| Parameter | Default | What Should Happen if Doubled |
|-----------|---------|-------------------------------|
| damage_increment | 0.002 | Expected to fail at 500 instead of 1000 |
| failure_threshold | 1.0 | Beam should survive twice as many cycles |

---

## KEY NUMBERS TO REMEMBER

- Center expected to fail at cycle **500** (default params)
- Edges expected at **50%** at cycle 500
- Double increment (0.004) --> expected fail at **250**
- Triple increment (0.006) --> expected fail at **167**

---

## 4 ENTITIES

| Entity | What It Will Be |
|--------|----------------|
| Bridge Beam | Main structure, 3 segments |
| Beam Segments | Left, Center, Right (tracked individually) |
| Load Cycles | Repeated load events (until failure) |
| Fatigue Damage State | 0.0 (new) to 1.0 (failed) per segment |

---

## VARIABLES

**Input:** damage_increment=0.002, failure_threshold=1.0, segment_factors=[0.5, 1.0, 0.5], num_segments=3
**State:** cycle (current iteration), damage[i] (per segment), status[i] (SAFE/WARNING/FAILED)
**Output:** Final damage, cycles to failure, damage history, saved PNGs
**Mode:** No max_cycles — runs until failure

---

## CREATE / ASSIGN / DECIDE / PROCESS / DISPOSE

| Step | What Will Happen |
|------|-----------------|
| **CREATE** | Initialize 3 beam segments |
| **ASSIGN** | Set damage=0, factors, status=SAFE |
| **PROCESS** | damage += increment × factor |
| **DECIDE** | damage >= threshold? More cycles? |
| **DISPOSE** | Mark FAILED; end; generate outputs |

Flow: CREATE → ASSIGN → [LOOP: PROCESS → DECIDE] → DISPOSE

---

## 6 OBJECTIVES (Memorize These)

1. Simulate cumulative fatigue damage (cycle-based)
2. Model position-dependent vulnerability (segment factors)
3. Detect and report structural failure (threshold)
4. Real-time animated 2D visualization
5. Generate 3D beam model
6. Enable parameter experimentation

---

## QUICK Q&A ANSWERS

**"Why normalized/simple model?"**
> M&S course -- focus is simulation concepts, not engineering math.

**"Can it be used for real bridges?"**
> No. Will be conceptual/educational only. Real analysis needs FEM, certified data, safety factors.

**"Why will center fail first?"**
> Midspan has highest bending stress in real beams. Factor 1.0 vs 0.5.

**"What is D = 1.0?"**
> Accumulated damage threshold = failure. Based on Miner's Rule.

**"What will user be able to change?"**
> 4 params: damage_increment, failure_threshold, num_segments, segment_factors. No max_cycles — runs until failure.

**"Fatigue vs static?"**
> Static = does ONE load break it? No. Fatigue = do THOUSANDS of loads accumulate to failure? Yes.

**"Why animation?"**
> Will let users watch degradation happen in real-time. Much more intuitive than static charts.

---

## KEY PHRASE REMINDERS

- Say "the simulation **will**..." not "the simulation does..."
- Say "we **expect** / **plan to**..." not "we found..."
- Say "the **proposed** model..." not "our model shows..."
- This is a **proposal** — the simulation has not been coded yet

---

*Stay calm. Follow the slides. Use future tense. You've got this!*
