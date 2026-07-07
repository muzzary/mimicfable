# Plan produced by the baseline condition (verbatim agent output)

Note: the baseline agent inherited the repo owner's global CLAUDE.md engineering
standards (visible in its references to phase logs, directory maps, and CI), so this
is not bare Opus. See the confound disclosure in the README.

## Overview

A single-user expense tracker in one Python file (`expenses.py`), standard library only, with JSON persistence. The plan is broken into dependency-ordered phases; each phase delivers a working, testable slice and proves the riskiest assumption early. The thin end-to-end slice (Phase 1) validates the whole pipeline - parse -> mutate -> persist -> read back - before any polish.

## Architecture at a glance

**Single file, layered internally so logic is testable without the CLI:**

- **Storage layer** - load/save the JSON file next to the script. One record shape: `{"date": "YYYY-MM-DD", "amount": <float>, "category": <str>, "note": <str>}`.
- **Domain layer** - pure functions: `add_expense`, `filter_by_month`, `sort_newest_first`, `summarize`. No I/O, no `sys.exit`.
- **Validation layer** - `parse_amount`, `parse_month`; raise a shared `UserError` on bad input.
- **CLI layer** - `argparse` subcommands; the only place that touches `stdout`/`stderr`/`sys.exit`.

**Key design decisions (surfaced for review):**
- **`argparse` with subparsers** rather than hand-rolled `sys.argv` parsing.
- **Amount stored as a number.** Recommendation: store rounded to 2 decimals, or use `decimal.Decimal` serialized as a string to avoid float rounding drift. Flagged as the one real correctness decision - see Phase 2 risks.
- **File path resolved relative to the script**, not the current working directory.
- **Missing/empty JSON file** -> empty expense list on load; a corrupt file should error loudly rather than silently wipe data.

## Phase 0 - Project scaffold

**Goal:** repo skeleton so every later phase lands into a clean, versioned structure.

- Create `expenses.py` (stub), `test_expenses.py`, `README.md`, `.gitignore`, and a directory-map note.
- Add a lightweight GitHub Actions workflow: run `pytest` and a linter on push.
- Initial commit.

**Acceptance test:** `python expenses.py` runs without crashing (prints usage/help); `pytest` collects the empty test file; CI workflow file is valid YAML.

## Phase 1 - Thin end-to-end slice: `add` + `list` (happy path only)

**Goal:** prove the full pipeline works before adding features. This is the riskiest-assumption phase - if persistence and round-tripping work, everything else is incremental.

- Storage: `load_expenses()` / `save_expenses()` against the JSON file.
- `add <amount> <category> [note]`: build a record with `date.today()`, append, save.
- `list`: load, sort newest first, print each row in a readable, stable format.
- Wire up `argparse` subparsers for `add` and `list` (no `--month` yet).

**Acceptance test (automated):** unit tests for `add_expense` and `sort_newest_first`; integration via subprocess into a temp dir: `add` then `list`, assert the row appears and the JSON file has the right content; add a second expense, assert newest-first order.

**Risk flagged:** date-only granularity means two expenses on the same day have no intra-day order. Recommend preserving insertion order (stable sort).

## Phase 2 - Input validation & error contract

**Goal:** satisfy the "bad input -> clear stderr message, exit 1" requirement, and harden storage.

- `parse_amount`: reject negative, zero, and non-numeric; lock the 2-decimal money decision.
- `parse_month`: validate `YYYY-MM` strictly (regex + month range 01-12).
- Unknown command / missing args: normalize argparse's exit 2 to the spec's exit 1 for `UserError`; decide how to treat argparse's own errors.
- Storage hardening: corrupt JSON -> clear `UserError`, never silently overwrite user data.

**Acceptance test (automated):** table-driven tests for each bad input asserting exit code 1 and non-empty stderr. Corrupt JSON errors rather than wiping data.

**Risk flagged:** the exit-code contract (spec wants 1) vs argparse's built-in exit 2.

## Phase 3 - `list --month` filtering

**Goal:** add month-scoped listing, reusing `parse_month` and `filter_by_month`.

**Acceptance test (automated):** seed expenses across two months; assert `--month` returns only matches, still newest-first; an empty month prints cleanly (exit 0).

## Phase 4 - `summary --month`

**Goal:** per-category totals plus grand total for a month; `--month` required per spec; deterministic category ordering.

**Acceptance test (automated):** known dataset -> exact per-category totals and grand total (including a floating-point-trap case like `0.10 + 0.20`); missing `--month` errors with exit 1; empty month handled gracefully.

## Phase 5 - Polish, docs, and final review

**Goal:** ship-ready. README with usage examples; full self-review pass; CI green; final manual-test handoff.

**Acceptance test:** full CLI walkthrough via subprocess against a temp file matches expected output; CI passes on push.

## Cross-cutting risks to settle before Phase 1

1. **Money representation** - float vs Decimal. Highest-impact correctness call.
2. **Exit codes** - reconcile spec's "exit 1" with argparse's exit 2.
3. **Same-day ordering** - define the tiebreaker for `list`.
4. **Corrupt-file policy** - error loudly, never silently overwrite.
5. **Concurrency** - single-user; no file locking planned; accepted limitation.

Each phase ends with: automated tests passing, a phase-log entry (what changed + how verified), and a commit/push.
