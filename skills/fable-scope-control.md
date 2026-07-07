---
name: fable-scope-control
description: Keeps changes scoped exactly to the request the way Fable 5 does - the diff maps one-to-one to the ask, adjacent problems become a follow-up list instead of silent extra changes. Use when fixing bugs or implementing features in existing code, especially in messy codebases where "while I'm here" temptations are strong.
---

# Fable-Style Scope Control

The measure of a good change: someone reading the diff can reconstruct the request from
it, and nothing else. Everything you touch beyond the ask is risk the user did not order.

## The core rule

**The diff maps 1:1 to the request.** Before presenting any change, read your own diff
and ask of every hunk: "which part of the request required this?" No answer = revert it.

## While working

- **Notice, don't fix.** You WILL see other problems: dead code, a bug in a neighboring
  function, missing validation, ugly naming. Do not touch them. Record each one and move on.
  Noticing is free; fixing is scope.
- **No "while I'm here."** No drive-by refactors, renames, reformatting, comment cleanups,
  or import reordering in code the request doesn't cover. Even correct improvements
  contaminate the diff, obscure the actual change in review, and can break things the
  user didn't ask you near.
- **True dependencies are the only exception.** If the fix genuinely cannot work without
  touching something adjacent (a caller must pass a new argument), touch the minimum and
  say explicitly in your report: "this required changing X because Y."
- **Ambiguity rule:** if an ambiguity in the request changes the design, state your
  assumption and proceed when the choice is reversible; stop and ask only when it is not.
- **Tests for the change are in scope.** A regression test for the thing you fixed is part
  of the ask. A test suite for the whole file is not.

## When you finish

Report in two strictly separated sections:

1. **Done**: what the request asked for, changed and verified.
2. **Noticed, not touched**: the adjacent problems you found, one line each, with file and
   line. The user decides what happens to them - that is their call, not yours.

Never let list 2 leak into list 1. An unrequested fix is not a bonus; it is unreviewed
change hidden inside a trusted one.

## Anti-patterns this replaces

| Habit | Replace with |
|---|---|
| "I also cleaned up X while I was there" | X goes in the noticed list |
| Fixing a second bug found mid-task | Report it; fix only if the user asks |
| Refactoring around the fix "for clarity" | The minimal diff that fulfills the ask |
| Silent formatting/rename churn in the diff | Zero hunks without a request behind them |
| Guessing at unstated wishes | State the assumption or ask |
