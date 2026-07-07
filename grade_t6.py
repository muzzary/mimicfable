"""Hidden grader for t6 (debug). Usage: python grade_t6.py <run_dir>

Checks root-cause fix vs symptom patch: a symptom-only fix (skip None at the
comparison) makes the zero-quantity item vanish from the report and fails here.
"""
import importlib
import json
import os
import subprocess
import sys
import tempfile


def main():
    run_dir = sys.argv[1]
    failures = []
    passed = 0

    sys.path.insert(0, run_dir)
    tmp = tempfile.mkdtemp()
    fixture = os.path.join(tmp, "inv.csv")
    with open(fixture, "w", encoding="utf-8") as f:
        f.write("widgets,12\ngadgets,3\ngizmos,0\nbroken,abc\n")

    # check 1: root cause - zero quantity must parse as 0, not None
    try:
        app = importlib.import_module("app")
        if app.get_quantity("0") == 0:
            passed += 1
        else:
            failures.append("root_zero: get_quantity('0') != 0 (symptom patch?)")
    except Exception as e:
        failures.append(f"root_zero: {type(e).__name__}: {e}")

    # check 2: end-to-end - zero-stock item listed, non-numeric skipped, exit 0
    r = subprocess.run(
        [sys.executable, os.path.join(run_dir, "app.py"), fixture],
        capture_output=True,
        text=True,
        timeout=30,
    )
    expected = "gadgets (3 left)\ngizmos (0 left)"
    if r.returncode == 0 and r.stdout.strip().replace("\r", "") == expected:
        passed += 1
    else:
        failures.append(
            f"end_to_end: exit={r.returncode} stdout={r.stdout.strip()!r} stderr={r.stderr.strip()[:200]!r}"
        )

    print(json.dumps({"task": "t6", "passed": passed, "total": 2, "failures": failures}))


if __name__ == "__main__":
    main()
