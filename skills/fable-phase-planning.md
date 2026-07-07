---
name: fable-phase-planning
description: Breaks a project or feature into phases the way Fable 5 does - every phase gets a concrete acceptance test before any code, dependency-ordered, riskiest assumption proven first via a thin end-to-end slice. Use when planning any multi-step build, when a task feels too big to start, or before writing code for anything beyond a small fix.
---

# Fable-Style Phase Planning

A plan is not a list of topics. It is a sequence of provable states. Produce plans with
these rules, in this order.

## 1. Restate the goal as an observable outcome

One sentence: what command, screen, or output proves the whole thing works when finished.
If you cannot state this, the requirements are not understood yet - resolve that first.

## 2. Find the riskiest assumption and schedule it FIRST

Ask: which part, if it turns out infeasible, kills or reshapes the project? (An unproven
API, a data source, a latency budget, a library capability.) Phase 1 must prove or break
that assumption with the smallest possible experiment - never leave the scary part for
phase 4, when three phases of work sit on top of it.

## 3. Build a walking skeleton before organs

The earliest possible phase should be a thin END-TO-END slice: input enters, crosses every
layer once, output exits - ugly, minimal, but connected. Integration problems are found by
integrating, not by finishing components in isolation and praying they join. Subsequent
phases thicken the skeleton one capability at a time.

## 4. Every phase states its acceptance test BEFORE its tasks

Format each phase as:

```
Phase N - <name>
  Proves: <the assumption or capability this phase establishes>
  Acceptance: <exact command or action> -> <observable result>
  Builds on: <phase numbers it needs>
```

The acceptance test is concrete and runnable ("`python app.py add 5 lunch` exits 0 and the
entry appears in `list`"), not aspirational ("data layer works"). **A phase that cannot
state a concrete acceptance test is not a phase** - split it, merge it, or admit it is
speculative and cut it.

## 5. Size phases to land in one sitting

Each phase must be small enough to implement, test, and commit in one continuous session.
A phase needing "several days" is a group of phases wearing a coat - split it. A phase
too small to have its own acceptance test belongs inside its neighbor.

## 6. State what is OUT of scope

End the plan with two short lists:
- **Out of scope**: tempting adjacent work the plan deliberately excludes.
- **Risks noticed**: loopholes or unknowns that could reorder later phases.

## Calibration

Skip this ceremony entirely for changes under ~30 lines in one file - go straight to
fix, test, verify. A plan for a rename is process theater.

## Anti-patterns this replaces

| Habit | Replace with |
|---|---|
| Phases named by component ("backend", "frontend", "polish") | Phases named by proven capability |
| Risky integration scheduled last | Riskiest assumption in phase 1 |
| "Then we test everything at the end" | An acceptance test per phase, run at that phase |
| Vague milestones ("core logic done") | Runnable command -> observable result |
| Plans that only add | An explicit out-of-scope list |
