"""Hidden grader for t4 (CLI). Usage: python grade_t4.py <run_dir>

Runs the agent's wordfreq.py as a subprocess against fixture files.
Prints one JSON line: {task, passed, total, failures, loc}.
"""
import json
import os
import subprocess
import sys
import tempfile

SAMPLE = "The cat sat. The cat ran! A dog barked, the dog."
EXPECTED_ALL = "the 3\ncat 2\ndog 2\na 1\nbarked 1\nran 1\nsat 1"
EXPECTED_TOP3 = "the 3\ncat 2\ndog 2"
EXPECTED_MINLEN3 = "the 3\ncat 2\ndog 2\nbarked 1\nran 1\nsat 1"


def run(script, *args):
    return subprocess.run(
        [sys.executable, script, *args], capture_output=True, text=True, timeout=30
    )


def loc(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip() and not line.strip().startswith("#"))


def main():
    run_dir = sys.argv[1]
    script = os.path.join(run_dir, "wordfreq.py")
    failures = []
    tmp = tempfile.mkdtemp()
    sample = os.path.join(tmp, "sample.txt")
    empty = os.path.join(tmp, "empty.txt")
    mixed = os.path.join(tmp, "mixed.txt")
    with open(sample, "w", encoding="utf-8") as f:
        f.write(SAMPLE)
    open(empty, "w").close()
    with open(mixed, "w", encoding="utf-8") as f:
        f.write("abc123 ABC def456def")

    checks = {
        "basic_counts": lambda: run(script, sample).stdout.strip().replace("\r", "")
        == EXPECTED_ALL,
        "top_n": lambda: run(script, sample, "--top", "3").stdout.strip().replace(
            "\r", ""
        )
        == EXPECTED_TOP3,
        "min_len": lambda: run(script, sample, "--min-len", "3").stdout.strip().replace(
            "\r", ""
        )
        == EXPECTED_MINLEN3,
        "missing_file_exit1": lambda: (
            lambda r: r.returncode == 1 and r.stderr.strip() != ""
        )(run(script, os.path.join(tmp, "nope.txt"))),
        "empty_file_exit0": lambda: (
            lambda r: r.returncode == 0 and r.stdout.strip() == ""
        )(run(script, empty)),
        "letters_only_split": lambda: run(script, mixed).stdout.strip().replace(
            "\r", ""
        )
        == "abc 2\ndef 2",
        "exit0_on_success": lambda: run(script, sample).returncode == 0,
    }
    passed = 0
    for name, fn in checks.items():
        try:
            if fn():
                passed += 1
            else:
                failures.append(f"{name}: wrong output")
        except Exception as e:
            failures.append(f"{name}: {type(e).__name__}: {e}")
    print(
        json.dumps(
            {
                "task": "t4",
                "passed": passed,
                "total": len(checks),
                "failures": failures,
                "loc": loc(script) if os.path.exists(script) else -1,
            }
        )
    )


if __name__ == "__main__":
    main()
