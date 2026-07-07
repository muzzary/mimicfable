---
name: fable-code-craft
description: Makes the model write and review code the way Fable 5 does - minimal purposeful code with zero speculative abstractions, reuse before writing new, match codebase idiom, and reviews that report only verified findings with concrete failure scenarios ranked by severity. Use before writing any implementation code and before committing or presenting a diff for review.
---

# Fable-Style Code Craft

Two workflows: **Writing** (before code exists) and **Reviewing** (before a diff ships). Apply both on every change.

## Writing: every line must earn its place

### Before writing
1. **Search before you create.** Grep for an existing helper, util, or pattern that already does the job. Writing a duplicate of something that exists is a bug, not a style issue.
2. **Read the neighbors.** Open 1-2 files adjacent to where your code will live. Your code must match their naming, error-handling style, and comment density - it should be impossible to tell which lines are new.
3. **Scope = the request, exactly.** Implement what was asked. Do not refactor adjacent code, rename things, or "improve while you're here" unless asked.

### While writing
- **YAGNI, enforced.** No config options nobody requested, no parameters with only one call-site value, no interfaces with one implementation, no wrapper layers, no "flexible" generalization for imagined future needs. Solve today's problem.
- **Every function needs a caller, every branch a reachable trigger, every import a use.** Unused = deleted before the diff is presented.
- **No new dependency when stdlib or an existing dependency covers it.** New deps require explicit user approval.
- **Fail loud.** No try/except or fallback added just to make an error disappear - swallowed errors are future debugging sessions. Handle a failure only where you can do something meaningful about it.
- **Comments state constraints the code can't show** (the "why", the invariant, the gotcha). Never what the next line does, never why your change is correct - that's reviewer-talk, noise after merge.
- **Delete, don't preserve.** Replaced code is removed, not commented out. No `_old` variants, no dead flags.

### The deletion test (run before presenting)
For each function, branch, parameter, and file you added ask: *if I deleted this, would the requested behavior break?* If no - delete it. Repeat until everything left is load-bearing.

## Reviewing: only verified findings, ranked by severity

### Pass 1 - Hunt (in severity order)
1. **Correctness** - logic errors, off-by-ones, unhandled edge cases (empty, null, concurrent, unicode), broken invariants.
2. **Security** - injected input, secrets in code, unsafe deserialization, missing auth checks on new paths.
3. **Reuse & simplification** - new code duplicating an existing helper; two near-identical branches that merge into one; an abstraction with a single user that should be inlined.
4. **Efficiency** - only where it's a real, reachable cost (N+1 queries, O(n^2) on unbounded input, work inside a hot loop). No micro-optimization nitpicks - unless timing IS correctness in this project (e.g. trading paths).

### Pass 2 - Verify (adversarial)
For each candidate finding, try to **refute it** against the actual code before reporting:
- Write the concrete failure scenario: *these inputs / this state -> this wrong output or crash.* If you cannot articulate one, it is not a finding - drop it.
- Check the "bug" isn't handled elsewhere (caller validates, type system prevents it, test covers it).

### Pass 3 - Report
- Most severe first. Each finding: one-sentence defect + failure scenario + file:line.
- High-confidence findings stated plainly; genuinely uncertain ones flagged briefly as uncertain - never dressed up as confident.
- **Zero style/formatting nitpicks.** Formatting is automated; commenting on it is noise.
- Nothing survived verification? Say "reviewed, clean" in one line - do not invent findings to look thorough.

## Anti-patterns this replaces

| Habit | Replace with |
|---|---|
| Helper/abstraction "for future flexibility" | Deletion test - inline it |
| Rewriting what an existing util already does | Grep first, reuse |
| try/except wrapping to look robust | Fail loud, handle only where meaningful |
| Comments narrating each line | Comments only for the "why" |
| Review padded with style nitpicks | Verified findings only, or "clean" |
| Reporting every hunch as a bug | Concrete failure scenario or drop it |
