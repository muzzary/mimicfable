# Review report: fable-code-craft skill condition (verbatim agent output)

Reviewed against the file. Findings below, most severe first.

## Findings

**1. Discount math is wrong - subtracts the percentage as a flat amount (correctness).** `review_target.py:5` - `d = p - discount_pct` computes `price minus discount_pct`, but the docstring promises a *percentage* discount. Correct form is `p * (1 - discount_pct/100)`. Failure scenario: `apply_discount([50], 10)` returns `[40]` (subtraction) instead of `[45]` (10% off). Every price where the discount isn't a coincidental match is wrong, and negative results appear whenever `discount_pct > price` (e.g. `apply_discount([5], 10)` -> `[-5]`). This corrupts the primary output for essentially all inputs.

**2. Mutable default argument leaks state across calls (correctness).** `review_target.py:1` - `log=[]` is evaluated once at definition, so the same list is shared by every call that doesn't pass `log`. Failure scenario: `apply_discount([1,2,3], 10)` then `apply_discount([4,5], 10)` - after the second call the shared `log` is `[3, 2]`, not `[2]`. Any caller relying on `log` to describe a single invocation gets accumulated history from all prior calls.

**3. Bare `except Exception: return 0` masks failures (correctness / fail-loud violation).** `review_target.py:12-15` - any error inside `apply_discount`/`sum` is swallowed and reported as a legitimate total of `0`. Failure scenario: `total_after_discount([100, None], 10)` raises a `TypeError` internally (subtracting/summing `None`), and the caller receives `0` - indistinguishable from a genuine zero total, hiding the bad input instead of surfacing it.

**4. `legacy_total` is dead and re-implements `sum()` (reuse / simplification).** `review_target.py:19-23` - no caller in the file, and the body is just `sum(prices)` written out as a manual loop. Low severity, but per the deletion test it is not load-bearing; if kept, it should be `return sum(prices)`.

Note: I reviewed the whole file (no other call sites are visible), so the "unused" judgment on `legacy_total` is scoped to this file - if an external module imports it, finding 4 downgrades to just the `sum()` duplication.
