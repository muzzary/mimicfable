"""Tests for wordfreq.py, driven through the CLI as the grader does."""
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent / "wordfreq.py")


def run(args, tmp_path, text=None):
    cmd = [sys.executable, SCRIPT]
    if text is not None:
        f = tmp_path / "in.txt"
        f.write_text(text, encoding="utf-8")
        cmd.append(str(f))
    cmd += args
    return subprocess.run(cmd, capture_output=True, text=True)


def test_spec_example(tmp_path):
    r = run([], tmp_path, "The cat sat. The cat ran! A dog barked, the dog.")
    assert r.returncode == 0
    assert r.stdout == "the 3\ncat 2\ndog 2\na 1\nbarked 1\nran 1\nsat 1\n"


def test_top(tmp_path):
    r = run(["--top", "2"], tmp_path, "The cat sat. The cat ran! A dog barked, the dog.")
    assert r.stdout == "the 3\ncat 2\n"


def test_top_zero(tmp_path):
    r = run(["--top", "0"], tmp_path, "a a b")
    assert r.returncode == 0
    assert r.stdout == ""


def test_min_len(tmp_path):
    r = run(["--min-len", "3"], tmp_path, "The cat sat. The cat ran! A dog barked, the dog.")
    # cat/dog (3), the (3) kept; "a" (1) dropped.
    assert r.stdout == "the 3\ncat 2\ndog 2\nbarked 1\nran 1\nsat 1\n"


def test_letters_only_separators(tmp_path):
    # digits/punctuation split words; case-folded.
    r = run([], tmp_path, "abc123def ABC-abc")
    assert r.stdout == "abc 3\ndef 1\n"


def test_nonexistent_file(tmp_path):
    missing = tmp_path / "nope.txt"
    r = subprocess.run([sys.executable, SCRIPT, str(missing)], capture_output=True, text=True)
    assert r.returncode == 1
    assert r.stdout == ""
    assert r.stderr.strip() != ""


def test_empty_file(tmp_path):
    r = run([], tmp_path, "")
    assert r.returncode == 0
    assert r.stdout == ""


def test_no_words_survive_filter(tmp_path):
    r = run(["--min-len", "10"], tmp_path, "the cat sat")
    assert r.returncode == 0
    assert r.stdout == ""
