# Review report: plain Opus baseline condition (verbatim agent output)

Reviewed `review_target.py` (24 lines, 3 functions). Findings by severity:

## High severity

**1. Discount math is wrong (line 5).** `d = p - discount_pct` subtracts the percentage as a flat amount, not a percentage. `apply_discount([100], 20)` returns `80` by luck, but `apply_discount([100], 10)` returns `90` when a 10% discount should give `90`... actually the coincidence only holds at specific values - `apply_discount([50], 20)` returns `30` where a 20% discount should be `40`. The function name and docstring ("Apply a percentage discount") promise percentage behavior. Correct form:
```python
d = p * (1 - discount_pct / 100)
```

**2. Mutable default argument (line 1).** `log=[]` is evaluated once at definition time and shared across every call. `log.append(len(prices))` accumulates across all invocations that don't pass an explicit `log`, so the list grows unboundedly and leaks state between unrelated callers. Standard fix:
```python
def apply_discount(prices, discount_pct, log=None):
    if log is None:
        log = []
```

## Medium severity

**3. Blanket exception swallowing (lines 12-16).** `total_after_discount` wraps the call in `except Exception: return 0`. This violates fail-loud/no-silent-failure principles: a `0` total is indistinguishable from a legitimate zero and from a real failure (bad input, type error). It hides the actual bug in #1/#2 and gives callers no signal. Catch only the specific expected error, or let it propagate with context.

## Low severity

**4. Dead / redundant code (lines 19-23).** `legacy_total` is unused by the other functions and merely reimplements the builtin `sum(prices)`. If nothing external depends on it, remove it; if kept for compatibility, it should be `return sum(prices)`.

**5. Missing docstrings (lines 11, 19).** `total_after_discount` and `legacy_total` have no docstrings, unlike `apply_discount`. Minor consistency/self-documentation gap.

## Note
The `log.append(len(prices))` side effect (line 7) is an unusual design - mixing a returned computation with hidden logging via a mutable param. Even after fixing #2, consider whether tracking call counts belongs here at all rather than in the caller.

Most important to fix before merge: **#1 (incorrect results)** and **#2 (shared-state bug)** - both produce silently wrong behavior in production.
