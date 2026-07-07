"""Hidden grader. Usage: python grade.py <t1|t2|t3> <run_dir>

Imports the agent's solution from run_dir and runs spec checks the agents never saw.
Prints one JSON line: {task, passed, total, failures, loc}.
"""
import importlib
import json
import sys


def check(name, fn, failures):
    try:
        fn()
        return True
    except Exception as e:
        failures.append(f"{name}: {type(e).__name__}: {e}")
        return False


def loc(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip() and not line.strip().startswith("#"))


def grade_t1(mod):
    checks = {}
    checks["unsorted_input"] = lambda: (
        mod.merge_intervals([[5, 7], [1, 3], [2, 4]]) == [[1, 4], [5, 7]]
    ) or (_ for _ in ()).throw(AssertionError("wrong result on unsorted input"))
    checks["touching_merge"] = lambda: (
        mod.merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]
    ) or (_ for _ in ()).throw(AssertionError("touching intervals not merged"))
    checks["empty"] = lambda: mod.merge_intervals([]) == [] or (_ for _ in ()).throw(
        AssertionError("empty input")
    )
    checks["single"] = lambda: mod.merge_intervals([[4, 9]]) == [[4, 9]] or (
        _ for _ in ()
    ).throw(AssertionError("single interval"))
    checks["contained"] = lambda: mod.merge_intervals([[1, 10], [2, 3]]) == [
        [1, 10]
    ] or (_ for _ in ()).throw(AssertionError("contained interval"))

    def no_mutation():
        orig = [[1, 3], [2, 6]]
        mod.merge_intervals(orig)
        assert orig == [[1, 3], [2, 6]], "input was mutated"

    checks["no_mutation"] = no_mutation
    return checks


def grade_t2(mod):
    s = mod.slugify
    cases = {
        "basic": lambda: s("Hello, World!") == "hello-world",
        "collapse_separators": lambda: s("  --Multiple---separators__here  ")
        == "multiple-separators-here",
        "unicode_nfkd": lambda: s("Crème brûlée") == "creme-brulee",
        "digits_kept": lambda: s("Python 3.13") == "python-3-13",
        "truncate_word_boundary": lambda: s("the quick brown fox", 12) == "the-quick",
        "truncate_exact_boundary": lambda: s("the quick brown", 9) == "the-quick",
        "long_first_word": lambda: s("abcdefghijkl", 5) == "abcde",
        "empty": lambda: s("") == "",
        "symbols_only": lambda: s("!!!") == "",
    }
    checks = {}
    for name, fn in cases.items():
        checks[name] = (
            lambda f=fn, n=name: f() or (_ for _ in ()).throw(AssertionError(n))
        )
    return checks


def grade_t3(mod):
    def raises_empty():
        try:
            mod.mean_of_list([])
        except ValueError:
            return
        raise AssertionError("mean_of_list([]) did not raise ValueError")

    def raises_no_match():
        try:
            mod.mean_of_positive([-1, -2])
        except ValueError:
            return
        raise AssertionError("mean_of_positive with no positives did not raise")

    return {
        "mean": lambda: mod.mean_of_list([1, 2, 3]) == 2
        or (_ for _ in ()).throw(AssertionError("mean")),
        "mean_positive": lambda: mod.mean_of_positive([-1, 2, 4]) == 3
        or (_ for _ in ()).throw(AssertionError("mean_positive")),
        "mean_negative": lambda: mod.mean_of_negative([-2, -4, 3]) == -3
        or (_ for _ in ()).throw(AssertionError("mean_negative")),
        "variance": lambda: abs(mod.variance([1, 2, 3]) - 2 / 3) < 1e-9
        or (_ for _ in ()).throw(AssertionError("variance")),
        "empty_raises": raises_empty,
        "no_match_raises": raises_no_match,
    }


TASKS = {
    "t1": ("intervals", grade_t1),
    "t2": ("slugify", grade_t2),
    "t3": ("stats", grade_t3),
}


def main():
    task, run_dir = sys.argv[1], sys.argv[2]
    module_name, grader = TASKS[task]
    sys.path.insert(0, run_dir)
    failures = []
    try:
        mod = importlib.import_module(module_name)
        checks = grader(mod)
        passed = sum(1 for name, fn in checks.items() if check(name, fn, failures))
        total = len(checks)
    except Exception as e:
        passed, total = 0, len(grader.__defaults__ or []) or -1
        failures.append(f"import/setup failed: {type(e).__name__}: {e}")
        total = 0
    result = {
        "task": task,
        "passed": passed,
        "total": total,
        "failures": failures,
        "loc": loc(f"{run_dir}/{module_name}.py"),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
