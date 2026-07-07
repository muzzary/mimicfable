# Task: simplify stats.py

`stats.py` works but has accumulated cruft. Simplify it.

## Constraints

1. Public behavior must NOT change: `mean_of_list(numbers)`, `mean_of_positive(numbers)`,
   `mean_of_negative(numbers)`, and `variance(numbers)` must keep their names, accept a
   single positional list argument, return the same values, and raise `ValueError` on
   empty/no-matching input exactly as before.
2. Anything not needed for that behavior may be changed or removed.
3. Standard library only.

## Deliverable

A simpler `stats.py` with identical public behavior. `test_basic.py` shows known-good
cases. Graded on: behavior preserved (test suite) and how much unnecessary code was
removed.
