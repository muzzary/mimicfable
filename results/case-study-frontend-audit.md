# Case study: frontend audit of a production commercial website

After the controlled benchmark, we pointed the fable-engineer agent at a real,
private commercial web product (a multi-app Django site in active use; name and
details withheld, it is a confidential project). The task: evaluate the entire
frontend for professionalism and generic "AI-generated" styling, under two hard
constraints, keep the existing color palette and keep the page structure. Assessment
only, no files edited.

This page reports what the agent achieved in that setting. Unlike the benchmark
tasks, nothing here was planted: every issue below existed in production code the
agent had never seen.

## What the agent found

- **A silently broken design-token layer, the root cause of the site's
  inconsistency.** The global stylesheet referenced a CSS custom-property type
  scale, a transition token, and several color tokens that were never defined
  anywhere in global scope. The agent counted the damage: over 100 declarations
  falling back to browser defaults, including 89 uses of an undefined font-size
  scale and 13 hover transitions that never animated. It also identified the
  human consequence: past developers had papered over the breakage with 35+
  `!important` overrides and inline styles, which is exactly what made the site
  look patched together.
- **Quantified, not vibes-based, findings.** 17 distinct border-radius values
  against 3 declared tokens, 74 box-shadow declarations, 111 gradients, 10
  backdrop blurs, a referenced monospace font that was never imported, and
  muted-text contrast of about 4.0:1 against a 4.5:1 accessibility floor.
- **The classic AI-styling tells, located precisely.** Emoji used as UI icons on
  the paid product surface directly beside a professionally drawn SVG icon set
  that already existed in the same codebase; a hero section stacking particles,
  animated glow lines, morphing shapes, and a grid overlay; around 18 dead
  placeholder links; five identical copy-pasted testimonial rows; and one
  headline typo on the landing page.
- **Every finding carried a file and line citation** and a concrete fix using
  only values from the site's existing palette, honoring both constraints.

## How the agent worked

- It loaded a frontend-engineering skill first, then read the base template, the
  global stylesheet's token layer, the shared components, and the flagship page
  before judging anything.
- It ranked all eight findings by visual impact and delivered them as a phased
  apply-order list, with the first four phases (one file plus a few templates)
  estimated to deliver about 80 percent of the perceived improvement.
- It flagged a non-obvious risk in its own top fix: defining the missing tokens
  would intentionally resize elements that currently render at fallback sizes,
  so it prescribed a live visual check before committing.
- It stated its limits unprompted: a static source assessment, contrast ratios
  computed rather than measured in a browser, and two secondary stylesheets read
  at token level only.

## Why this is here

The controlled benchmark showed the agent ties plain Opus on small planted tasks
and differentiates on discipline. This case study is the complementary evidence:
on a real, messy, unfamiliar production codebase, the discipline is the product.
The agent did not stop at "the hero looks generic", it traced the generic look to
a broken token foundation, measured it, and handed back an implementation-ready,
constraint-respecting plan with its own uncertainty stated.

Same honesty as the benchmark: this is one run on one codebase, the codebase
cannot be shared, and you have to take our word for the specifics. Treat it as a
qualitative demonstration, not a metric.
