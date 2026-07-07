# Task: plan an expense tracker CLI

Produce an implementation plan for the following project. Do NOT write the
implementation - the plan itself is the deliverable.

## Product spec

A single-user command-line expense tracker, Python, standard library only:

- `expenses.py add <amount> <category> [note]` records an expense with today's date.
- `expenses.py list [--month YYYY-MM]` prints expenses, newest first.
- `expenses.py summary --month YYYY-MM` prints per-category totals and a grand total.
- Data persists between runs in a JSON file next to the script.
- Bad input (negative amount, malformed month, unknown command) prints a clear error
  to stderr and exits 1.

## Deliverable

An implementation plan, broken into phases, as your final message.
