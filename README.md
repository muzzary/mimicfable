# fable-engineer: a disciplined coding agent, benchmarked honestly

This repo contains a custom Claude Code subagent called **fable-engineer** and a small,
fully reproducible benchmark comparing it against plain Claude Opus on identical coding
tasks. Every number below comes from real runs, graded by hidden test suites the agents
never saw. Nothing is projected, extrapolated, or borrowed from other benchmarks.

## Install

One command, needs Node 16+ and git:

```
npx github:muzzary/mimicfable
```

That installs the fable-engineer agent into `~/.claude/agents/` and all four skills
into `~/.claude/skills/`, where Claude Code picks them up on your next session.
Options:

```
npx github:muzzary/mimicfable --agent       agent only
npx github:muzzary/mimicfable --skills      skills only
npx github:muzzary/mimicfable --uninstall   remove everything it installed
```

### Other coding agents (Codex, Copilot, Cursor, Gemini CLI)

The same discipline works outside Claude Code. `PORTABLE.md` is a tool-agnostic
version of the agent and all four skills, and the installer knows where each tool
reads its instructions:

```
npx github:muzzary/mimicfable --codex       OpenAI Codex CLI (global ~/.codex/AGENTS.md)
npx github:muzzary/mimicfable --copilot     GitHub Copilot (this project's .github/copilot-instructions.md)
npx github:muzzary/mimicfable --cursor      Cursor (this project's .cursor/rules/)
npx github:muzzary/mimicfable --gemini      Gemini CLI (global ~/.gemini/GEMINI.md)
npx github:muzzary/mimicfable --agents-md   plain AGENTS.md in this project (the emerging universal standard)
```

Flags combine freely (`--codex --cursor`). Project-scope flags write relative to the
directory you run the command in. If the target file already exists, the instructions
are added inside `<!-- mimicfable -->` marker comments: your existing content is never
touched, reruns update only the marked block, and `--uninstall` removes only that
block. That safety behavior is tested.

One honest note: the benchmark in this repo was run on Claude models only. The
portable instructions carry the same rules to other tools, but we have not measured
their effect on Codex, Copilot, Cursor, or Gemini.

No npm registry involved and no dependencies: npx pulls this repo and runs a small
copy script (`bin/install.js`, readable in one sitting). Prefer not to pipe code from
the internet? Clone the repo, read the script, then run `node bin/install.js`
yourself. Rerunning updates files in place.

After installing for Claude Code: delegate big tasks with "use the fable-engineer
agent to ..." and invoke skills inline with `/fable-problem-solving`,
`/fable-code-craft`, `/fable-phase-planning`, or `/fable-scope-control`.

## What the agent is

fable-engineer is a system prompt (an agent definition) that makes Claude Opus work the
way Anthropic's Fable 5 model works: gather context before acting, commit to one
diagnosis instead of hedging, keep every line of code load bearing, verify by actually
running things, and report outcomes first. The definition lives in
`fable-engineer.md` and runs on the standard Claude Code Agent tool.

## How the benchmark works

- Two conditions, same model (`claude-opus-4-8`), same task prompts, isolated git repos.
  The only difference: one condition adopts the fable-engineer definition, the other gets
  no extra instructions.
- Four task types: a bug fix with three planted bugs, a feature built from a written spec
  (run three times per condition), a refactor of an 87 line file, and a multi requirement
  CLI tool graded end to end through subprocess calls.
- Grading is automated and hidden. The graders were validated before any run: they fail
  the original buggy code and pass a reference solution.
- 12 runs total (plus one run that stalled at startup for harness reasons and was
  restarted; its wasted tokens are excluded and disclosed).

## Results

### Correctness, hidden checks passed

| Task | fable-engineer | plain Opus |
|---|---|---|
| Bug fix (6 checks) | 6/6 | 6/6 |
| Feature, 3 runs (9 checks each) | 27/27 | 27/27 |
| Refactor (6 checks) | 6/6 | 6/6 |
| CLI tool (7 checks) | 7/7 | 7/7 |
| **Total** | **46/46** | **46/46** |

### Everything else

| Metric | fable-engineer | plain Opus |
|---|---|---|
| Committed a regression test suite | 4 of 7 tasks | 1 of 7 tasks |
| Feature solution size, 3 runs (LOC) | 11 / 14 / 20 (mean 15.0) | 21 / 14 / 18 (mean 17.7) |
| Other solutions (LOC) | 14 / 12 / 32 | 15 / 14 / 32 |
| Output tokens, all runs | ~300k | ~272k (about 10% cheaper) |
| Bugs caught by its own tests before commit | 1 (truncation edge case) | 0 reported |

## What we actually learned

**Correctness was a tie.** Plain Opus aced every task on its own. On single file,
well specified work, the definition adds no correctness. We say that plainly because
it is what the data shows, and because it makes the rest of the findings believable.

**The reliable, replicated difference is test discipline.** The fable agent left behind
committed regression test suites in 4 of 7 runs. Plain Opus verified its work with
throwaway checks and committed tests once. Both approaches pass today's grader. The
difference shows up next month, when the next change lands on code that either has a
safety net or does not. In one run the agent's own edge case tests caught a real
truncation bug before commit, which is that safety net working in real time.

**The code size effect is real but modest, and we corrected ourselves on it.** Our first
round showed the fable version of the feature at less than half the size of the baseline
(11 vs 21 lines). Two repeat runs shrank that gap to roughly 15 percent on average, with
overlap between conditions. The first number was real but lucky. With three runs each,
the honest claim is: slightly leaner code, consistently, not dramatically.

**The cost is about 10 percent more tokens and a bit more wall time**, spent on baseline
test runs before changes, written test suites, and final verification. Whether that
trade is worth it depends on the work: for throwaway scripts, no. For code you will
still be running next month, the committed tests alone likely pay for it.

## Where to use it, and where not to

Use fable-engineer for:

- Any project you will still be running next month. The committed regression tests are
  the whole point, and they compound: each phase lands with a safety net the next
  phase runs against.
- Multi phase or multi file work, where one change can quietly break another.
- Code where being wrong is expensive: trading logic, data pipelines, anything handling
  money or user data. The verify before done habit exists for exactly this.
- Refactors of working code, because it establishes a passing test baseline before
  touching anything.

Skip it for:

- Throwaway scripts, quick experiments, one off data munging. The discipline is pure
  overhead there; plain Opus is cheaper, faster, and just as correct on small tasks.
- Simple questions and small clear fixes. You do not need a phase plan to rename a
  variable.
- Anything where you just want a fast draft you plan to rewrite anyway.

Rule of thumb: if you would delete the code tomorrow, skip the agent. If the code has
a future, use it.

## The companion skills

The `skills/` folder holds four lighter weight versions of the same habits, meant for
your main session rather than a delegated agent. Skills shape how the model you are
already talking to works; the agent is for handing off whole tasks. Do not stack them
on top of the agent, since the agent already contains everything the skills say.

- **fable-problem-solving**: gather context first, commit to one diagnosis, act,
  verify with evidence, report outcome first. Use it for debugging and everyday tasks.
- **fable-code-craft**: write minimal load bearing code, and review with a
  no-nitpicks, failure-scenario-or-drop-it standard. Use it when writing or
  reviewing code.
- **fable-phase-planning**: plan as a sequence of provable states. Every phase gets a
  runnable acceptance test before any code, the riskiest assumption is proven first,
  and a thin end to end slice comes before components. Use it before any multi step
  build.
- **fable-scope-control**: the diff maps one to one to the request. Adjacent problems
  get noticed and reported, never silently fixed. Use it when changing existing code,
  especially messy code.

We tested both the same way as the agent, one run each against plain Opus:

- **Review test** (a file with three planted bugs plus plenty of style bait): both
  conditions found all three bugs and the dead code. The difference was report
  quality. The skill guided review attached a concrete failure scenario to every
  finding and reported zero style nitpicks. The plain review included a docstring
  nitpick and reasoned less cleanly through the arithmetic bug. Both raw reports are
  in `results/` so you can judge for yourself.
- **Debugging test** (a crash whose root cause hides in a truthiness bug that turns a
  quantity of 0 into "missing"): a tie. Both conditions found the root cause and
  fixed it properly, 2/2 hidden checks each.

- **Scope test** (fix one discount bug in a repo full of bait: dead functions, a fake
  email validator, clunky loops): both conditions fixed the bug 4/4 and kept the diff
  to the same 4 lines in one file. Two differences showed up in the git evidence. The
  skill run delivered a separated "noticed, not touched" list naming the bait and left
  build artifacts untracked; the baseline mentioned nothing it saw and committed a
  compiled `.pyc` cache file into the repo.
- **Planning test** (same CLI spec planned by both): both plans were strong and both
  put a thin end to end slice first. The skill plan was stricter where the skill
  demands it: an observable definition of done up front, a runnable acceptance test
  on all six phases (the baseline had two phases with vague acceptance), an explicit
  six item out of scope list (the baseline had none), and sharper risk calls like
  atomic file writes and timezone edge cases. Both plans are published verbatim in
  `results/` so you can judge them yourself.

Honest read: on single runs, the skills sharpen output discipline (no noise, explicit
failure scenarios, separated scope reporting, stricter plan structure) more than they
change what gets found or fixed. Opus finds the bugs either way; the skills change
what it does around them.

## Real-world spot check (beyond the benchmark)

We also ran the agent against a real, private commercial website (a confidential
project, so no name and no code, only what the agent achieved). Nothing was planted;
the codebase was messy production work the agent had never seen. In one
assessment-only pass it:

- traced the site's generic "AI-assembled" look to a root cause nobody had spotted:
  a silently broken CSS design-token layer, with 100+ declarations referencing
  custom properties that were never defined, and the 35+ `!important` overrides
  developers had piled on to compensate
- quantified the inconsistency instead of hand-waving it: 17 border-radius values
  against 3 declared tokens, 111 gradients, 74 shadows, a referenced font that was
  never imported, and text contrast below the accessibility floor
- located the classic AI tells with file and line citations: emoji used as icons
  next to an existing professional SVG set, a particles-and-glow hero stack, dead
  placeholder links, cloned testimonials, one landing-page typo
- delivered a phased fix plan whose first four phases touch one shared stylesheet
  plus a few templates for roughly 80 percent of the improvement, all within the
  owner's hard constraints (same palette, same structure)
- flagged the risk inside its own top recommendation and stated what it had not
  verified, unprompted

Details in `results/case-study-frontend-audit.md`. Same honesty rule as everywhere
else in this repo: it is one run on one codebase we cannot show you, so treat it as
a qualitative demonstration, not a metric.

## A confound we found and want you to know about

Partway through the skill tests we noticed the "plain Opus" baseline referencing
phase logs, directory maps, and manual test handoffs. Those terms come from the repo
owner's global CLAUDE.md, which Claude Code injects into every agent on the machine,
baselines included. So every baseline in this benchmark is really "Opus plus a strong
personal engineering standards file", not bare Opus.

Two consequences, stated plainly. First, the deltas reported here are measured against
a disciplined baseline, so they likely UNDERSTATE what the agent and skills add over a
stock setup. Second, a good CLAUDE.md already buys real discipline on its own, which
is itself a useful finding. We chose to disclose rather than rerun, since the
disciplined baseline is also the realistic one: nobody runs these tools with an empty
config.

## Limitations, stated up front

- Three runs on one task, one run on the others. Small samples; treat exact
  percentages loosely. The direction of the findings replicated; the magnitudes wobble.
- Tasks are small, single file, and well specified. This is the setting least favorable
  to the agent, since its discipline targets long, multi phase project work that this
  suite does not yet exercise.
- The tasks, graders, and agent definition were authored with the same model family.
  Grading itself is fully automated and objective.

## Reproduce it

1. Put `fable-engineer.md` in `~/.claude/agents/`.
2. Recreate the task folders from `tasks/`, each as its own git repo.
3. Run each task through the Claude Code Agent tool (model `opus`) twice: once with
   "adopt fable-engineer.md as your operating instructions" prefixed to the prompt,
   once without.
4. Grade with `python grade.py <t1|t2|t3> <run_dir>`, `python grade_t4.py <run_dir>`,
   and `python grade_t6.py <run_dir>`. The review test (t5) has no automated grader;
   compare reports against the three planted bugs in `tasks/t5_review/review_target.py`
   (flat subtraction instead of percentage, mutable default argument, swallowed
   exception) and count style nitpicks yourself.
5. Delivered solutions and verbatim review reports from our runs are in `results/`
   if you want to check our grading.

See `BENCHMARK.md` for the full methodology and per run details.
