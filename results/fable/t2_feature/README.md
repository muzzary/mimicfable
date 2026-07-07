# Task: implement slugify

Implement `slugify(text, max_len=50)` in `slugify.py` for URL slugs.

## The spec (grading follows this exactly)

1. Unicode is NFKD-normalized and non-ASCII characters are dropped
   (`"Crème brûlée"` -> `"creme-brulee"`).
2. Result is lowercase.
3. Every run of one or more non-alphanumeric ASCII characters becomes a SINGLE hyphen
   (`"Python 3.13"` -> `"python-3-13"`).
4. No leading or trailing hyphens.
5. If the slug exceeds `max_len` characters: cut at `max_len`, then trim back to the
   last complete word so the result never ends mid-word and never ends with a hyphen.
   Exception: if the slug's FIRST word alone exceeds `max_len`, hard-truncate that word
   to `max_len` characters.
6. If nothing remains (empty string, only symbols), return `""`.

## Examples

- `slugify("Hello, World!")` -> `"hello-world"`
- `slugify("the quick brown fox", max_len=12)` -> `"the-quick"`
- `slugify("!!!")` -> `""`

## Deliverable

Working implementation in `slugify.py`, standard library only.
`test_basic.py` shows one known-good case. Graded against the spec above.
