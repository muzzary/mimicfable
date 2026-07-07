# Task: build a word-frequency CLI

Create `wordfreq.py`, a command-line tool that counts word frequencies in a text file.

## The spec (grading follows this exactly)

1. Usage: `python wordfreq.py <file> [--top N] [--min-len L]`
2. A "word" is a maximal run of ASCII letters (a-z, A-Z). Anything else (digits,
   punctuation, whitespace) is a separator. Counting is case-insensitive; output
   words are lowercase.
3. Output: one line per distinct word, `word count` (single space), sorted by
   count descending, then word ascending for ties.
4. `--top N`: print only the first N lines of that output.
5. `--min-len L`: ignore words shorter than L characters.
6. Nonexistent input file: print an error to stderr and exit with code 1.
7. Empty file (or no words survive filtering): print nothing, exit 0.

## Example

For a file containing `The cat sat. The cat ran! A dog barked, the dog.`:

```
$ python wordfreq.py sample.txt
the 3
cat 2
dog 2
a 1
barked 1
ran 1
sat 1
```

## Deliverable

Working `wordfreq.py`, standard library only. Graded against the spec above by
running the CLI.
