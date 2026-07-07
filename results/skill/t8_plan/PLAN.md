# Plan produced under the fable-phase-planning skill (verbatim agent output)

## Observable outcome (what proves the whole thing works)

Running `python expenses.py add 12.50 groceries "milk and eggs"` then `python expenses.py summary --month 2026-07` prints `groceries 12.50` and a matching grand total, with the data surviving a second, separate process invocation. When that round-trip works and bad input exits 1 with a stderr message, the tool is done.

## Riskiest assumption

The scary part here is **not** the arithmetic or argument parsing - those are routine. The real risk is the **persistence + process-boundary contract**: every command is a fresh process that must load prior state from JSON, mutate it, and write it back without corrupting the file on bad input or a mid-write crash. If the read/modify/write cycle is wrong, every feature built on it is wrong. So Phase 1 proves that cycle end-to-end with a single command, before `list`, `summary`, or validation exist.

## Phase 1 - Walking skeleton: add + persist round-trip

```
Phase 1 - add writes to JSON and it survives the process
  Proves: the load -> mutate -> save cycle works across separate process invocations
          (the riskiest contract), and the CLI dispatch wiring is connected end-to-end.
  Acceptance: `python expenses.py add 12.50 groceries "milk"` exits 0; the JSON file
              next to the script now contains one entry with amount 12.50, category
              groceries, note "milk", and today's date. Running the same command a
              second time yields a file with TWO entries (proves append, not overwrite).
  Builds on: nothing.
```

Tasks: minimal `argparse` (or manual `sys.argv`) dispatch recognizing only `add`; a load function that returns `[]` when the file is missing; append the record; write back with `json.dump`. Store the JSON file path as `os.path.join(dirname(__file__), "expenses.json")`. No validation, no other subcommands yet - ugly but connected across all layers (CLI -> logic -> disk).

This is the thin end-to-end slice: input enters, crosses parse/store/persist once, and the effect is observable on disk.

## Phase 2 - list (read path + ordering)

```
Phase 2 - list prints stored expenses newest first
  Proves: the read/format path and the newest-first ordering contract.
  Acceptance: after adding three expenses, `python expenses.py list` prints all three,
              with the most recently added at the top, one per line including amount,
              category, date, and note.
  Builds on: Phase 1.
```

Tasks: add `list` to dispatch; load, sort newest-first, format each row. Decide the ordering key now (insertion order reversed, or by date + a stable tiebreaker) and lock it - `summary` and the `--month` filter will lean on the same records. No month filter yet.

## Phase 3 - month filtering on list

```
Phase 3 - list --month filters by month
  Proves: the YYYY-MM filter predicate that summary will reuse.
  Acceptance: with expenses across two different months on disk,
              `python expenses.py list --month 2026-07` prints only the July 2026
              entries, still newest first; a month with no expenses prints nothing
              (or an empty-state line) and exits 0.
  Builds on: Phase 2.
```

Tasks: add the optional `--month` flag; filter records whose date starts with the given `YYYY-MM`. Keep filtering as a small reusable helper - Phase 4 calls it.

## Phase 4 - summary (aggregation)

```
Phase 4 - summary totals per category and overall
  Proves: the aggregation logic over the filtered month set.
  Acceptance: given known July expenses (e.g. groceries 12.50 + groceries 7.50 +
              transport 4.00), `python expenses.py summary --month 2026-07` prints
              `groceries 20.00`, `transport 4.00`, and a grand total `24.00`,
              exiting 0.
  Builds on: Phase 3 (reuses the month filter).
```

Tasks: add `summary` requiring `--month`; reuse the Phase 3 filter; sum per category into a dict and a grand total; format with 2-decimal money output. Use integer-cents or `Decimal` internally if float rounding shows up in the acceptance numbers - decide here, where the totals are first observable.

## Phase 5 - input validation + error contract (harden every entry point)

```
Phase 5 - bad input fails loud on stderr with exit 1
  Proves: the defensive error boundary across all commands; no silent failures,
          no corrupted JSON file on bad input.
  Acceptance: each of the following prints a clear message to STDERR (not stdout)
              and exits 1, AND leaves the JSON file unchanged:
                - `python expenses.py add -5 groceries`        (negative amount)
                - `python expenses.py add abc groceries`       (non-numeric amount)
                - `python expenses.py summary --month 2026-13` (malformed month)
                - `python expenses.py frobnicate`              (unknown command)
              A corrupt/unreadable JSON file also errors clearly rather than crashing
              with a raw traceback.
  Builds on: Phases 1-4.
```

Tasks: validate amount (numeric, positive) before write; validate `--month` against `YYYY-MM` shape and valid month range; reject unknown commands; wrap the JSON load in a try/except that reports a clear message on malformed data. Route all these to `sys.stderr` + `sys.exit(1)`. Validation goes before persistence so bad input never touches the file (this is why hardening comes after the write path exists - it can now be tested against a real file).

## Phase 6 - regression test suite + CI

```
Phase 6 - automated tests lock in every phase
  Proves: all acceptance behaviors are captured as repeatable tests and stay green.
  Acceptance: `python -m unittest` (or `pytest`) runs green, covering the add/list/
              summary happy paths, newest-first ordering, month filtering, summary
              totals, and every Phase 5 error case (exit code + stderr). Tests use a
              temp-dir JSON file, not the real one. A lightweight GitHub Actions
              workflow runs the suite on push.
  Builds on: Phases 1-5.
```

Tasks: drive the CLI via `subprocess` (asserting exit codes and stderr) or by calling the entry function with a redirected data path; point the data file at a `tempfile` dir per test for isolation; add a minimal `.github/workflows` that runs the tests on every push.

> Note on sequencing: per my standing workflow, each phase writes its own tests at its end and commits before the next begins - Phase 6 is the consolidation/CI pass, not the first time tests appear.

## Out of scope

- Editing or deleting existing expenses.
- Multiple users, accounts, or currencies (single-user, single implied currency).
- Budgets, recurring expenses, charts, or export to CSV/PDF.
- Concurrent access / file locking (single-user, serial invocations assumed).
- Config files, environment-variable overrides for the data path (tests aside), or a custom storage location.
- Database or any non-stdlib dependency - JSON + standard library only, as specified.

## Risks noticed

- **Float money rounding.** Summing floats (12.50 + 7.50) can produce `20.000000001`-style artifacts. If Phase 4's acceptance numbers wobble, switch internal representation to integer cents or `Decimal`. Flagged early so it doesn't silently corrupt totals.
- **Date source & timezone.** "Today's date" uses local system date; a user near midnight in another timezone could see an off-by-one day. Acceptable for a single-user local tool, but it's the one place `add` is non-deterministic - tests should inject/mock the date rather than assert on the live clock.
- **Ordering ambiguity.** All expenses on the same day have identical dates; "newest first" then depends on insertion order. Phase 2 must fix a deterministic tiebreaker (append order) or `list`/`summary` output becomes unstable. If ordering later needs to be by timestamp, records may need a stored insertion time - a possible reshaping of the Phase 1 record shape.
- **Partial-write corruption.** A crash mid-`json.dump` could truncate the file. If this proves to matter, write to a temp file and atomically replace - noted, but deliberately deferred unless Phase 5's "file unchanged on error" test surfaces it.
- **Note argument quoting.** A multi-word note requires shell quoting; an unquoted `add 5 lunch team outing` will misparse. Phase 1's arg model should decide whether `note` is a single positional (quoted) or joined remainder, since it affects the `add` signature everywhere downstream.

Calibration note: this is a multi-command, multi-phase build with a real persistence contract, so the full phase ceremony applies - it is well above the ~30-line single-file threshold where planning would be theater.
