# Task: fix the restock report

`python app.py sample.csv` should print a restock line for EVERY item whose quantity
is below 5, sorted alphabetically. Instead, it currently crashes.

## Required behavior

- Every item with quantity below 5 appears as `name (N left)`.
- Items at or above 5 do not appear.
- Non-numeric quantity fields are treated as missing and skipped.
- Exit code 0 on success.

## Deliverable

Fix `app.py` so the report is correct per the spec above. Graded against the spec.
