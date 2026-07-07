# fable-engineer agent — benchmark

A controlled comparison of the **fable-engineer** Claude Code subagent (Claude Opus running
under a Fable-5-style operating definition) against **plain Claude Opus** with no definition,
on identical coding tasks.

> **What this is:** a small, self-run, reproducible eval — n = 1 run per condition per task,
> graded by hidden test suites the agents never saw.
> **What this is not:** an industry benchmark (SWE-bench etc.). No claim of statistical
> significance is made. Treat it as a controlled demonstration, not a leaderboard score.

## Setup

- **Date:** 2026-07-07 · **Model (both conditions):** `claude-opus-4-8` via the Claude Code
  Agent tool · **Machine:** Windows 10, Python 3.13.3, git 2.49
- **Conditions:** identical task prompts and isolated git repos. The *fable* condition's
  prompt additionally instructed the agent to adopt `fable-engineer.md` as its operating
  instructions. The *baseline* condition received no extra instructions.
- **Grading:** hidden checker (`grade.py`) with spec checks the agents never saw, validated
  before the runs (it fails the original buggy code and passes a reference solution).
  Lines of code counted as non-blank, non-comment lines of the solution file.

## Tasks

| Task | Type | Hidden checks |
|---|---|---|
| t1 | **Bug fix** — `merge_intervals` with 3 planted bugs (missing sort, touching intervals not merged, input mutation) | 6 |
| t2 | **Feature from spec** — implement `slugify(text, max_len)` incl. NFKD unicode handling and word-boundary truncation | 9 |
| t3 | **Refactor** — simplify an 87-line `stats.py` (dead class, unused params, duplicated loops) without changing public behavior | 6 |

## Results

### Correctness (hidden checks passed)

| Task | fable-engineer | baseline Opus |
|---|---|---|
| t1 bug fix | **6/6** | **6/6** |
| t2 feature | **9/9** | **9/9** |
| t3 refactor | **6/6** | **6/6** |
| **Total** | **21/21** | **21/21** |

Both conditions found all three planted bugs in t1, implemented the full t2 spec including
the truncation edge cases, and preserved exact behavior (including error messages) in t3.

### Code size of the delivered solution (LOC, lower = leaner)

| Task | fable-engineer | baseline Opus | difference |
|---|---|---|---|
| t1 `intervals.py` | **14** | 15 | −7% |
| t2 `slugify.py` | **11** | 21 | **−48%** |
| t3 `stats.py` | **12** | 14 | −14% |

### Cost and process

| Metric | fable-engineer | baseline Opus |
|---|---|---|
| Output tokens (3 tasks) | 147,377 | 134,296 (**−9% cheaper**) |
| Wall time (3 tasks) | 292 s | 213 s |
| Tool calls (3 tasks) | 26 | 20 |
| Committed work per task | 2 commits each | 2 commits each |
| Added regression test files | t1, t2 | t1 |
| Ran baseline tests *before* refactoring (t3) | yes | not reported |
| Verified error-message equality in refactor | yes | yes |

## Honest findings

1. **Correctness tied at 21/21.** On tasks of this size, plain Opus is already strong enough
   that the definition adds no correctness headroom. Differences would need harder,
   longer-horizon tasks to surface.
2. **The definition's measurable effect is leaner code** — most visible on the
   green-field task (t2: 11 vs 21 LOC for identical behavior, −48%). This matches the
   definition's deletion-test rule.
3. **The discipline costs ~10% more tokens and ~37% more wall time**, spent on extra
   verification (pre-change baseline test runs, added spec test suites, final-gate checks).
4. **Process differences:** the fable agent wrote committed regression tests on 2 of 3
   tasks vs 1 of 3, and established a test baseline before refactoring — behaviors the
   definition explicitly demands.

## Round 2 (same day): repeats + a harder task

To test whether round 1 held up, we ran 6 more runs: t2 twice more per condition
(n = 3 total on the headline LOC finding) and a new task **t4** — a word-frequency CLI
with 7 spec requirements, graded end-to-end via subprocess (`grade_t4.py`).

| Run | fable checks | fable LOC | baseline checks | baseline LOC |
|---|---|---|---|---|
| t2 run 2 | 9/9 | 14 | 9/9 | 14 |
| t2 run 3 | 9/9 | 20 | 9/9 | 18 |
| t4 CLI | 7/7 | 32 | 7/7 | 32 |

**Corrections this forced:**
- The round-1 t2 LOC gap (11 vs 21, −48%) did **not** fully replicate. Across n = 3,
  fable mean is 15.0 LOC vs baseline 17.7 (−15%), with overlapping ranges. The honest
  claim is "slightly leaner, consistently" — not "half the code."
- Correctness stayed tied: cumulative **46/46 vs 46/46** across all 12 runs.
- The **replicated** difference is test discipline: fable committed regression test
  suites in 4 of 7 tasks (verified via `git ls-files`), baseline in 1 of 7. In t2 run 3,
  the fable agent's own edge-case tests caught a real truncation bug pre-commit and it
  reported the bug unprompted.
- Token cost held at ~+10% (fable ~300k vs baseline ~272k across all runs).
- Disclosure: one fable run (t2 run 2) stalled at startup with zero tool calls (harness
  hiccup, ~35k tokens) and was restarted; the stalled attempt's tokens are excluded
  from the totals above and disclosed here.

## Limitations

- n = 1 run per cell; LLM output varies between runs. Token/time deltas within ~±20%
  should not be over-read.
- Tasks are small (single-file, ≤90 LOC). The definition targets multi-phase project work,
  which this suite does not exercise.
- Tasks and grader were authored by the same (different, stronger) model that wrote the
  agent definition; grading itself is fully automated and objective.

## Reproducing

1. Install the agent definition at `~/.claude/agents/fable-engineer.md`.
2. Recreate the three task folders from the specs above (or reuse this repo's `tasks/`).
3. Run each task twice via the Claude Code Agent tool (model `opus`): once prefixed with
   "adopt fable-engineer.md as your operating instructions", once without.
4. Grade with `grade.py <task> <run_dir>`.
