from slugify import slugify


def test_unicode_nfkd():
    assert slugify("Crème brûlée") == "creme-brulee"


def test_symbol_runs_collapse():
    assert slugify("Python 3.13") == "python-3-13"
    assert slugify("a --- b") == "a-b"


def test_no_edge_hyphens():
    assert slugify("  --hello--  ") == "hello"


def test_truncate_to_word():
    assert slugify("the quick brown fox", max_len=12) == "the-quick"


def test_truncate_cut_on_boundary():
    # Cut lands right after a complete word (next char is the hyphen).
    assert slugify("the quick brown fox", max_len=9) == "the-quick"


def test_truncate_cut_on_hyphen():
    # slug[max_len] is mid-word, slug[:max_len] ends with a hyphen.
    assert slugify("the quick brown fox", max_len=10) == "the-quick"


def test_first_word_too_long():
    assert slugify("supercalifragilistic", max_len=5) == "super"


def test_empty_and_symbols_only():
    assert slugify("") == ""
    assert slugify("!!!") == ""


def test_non_ascii_only():
    assert slugify("日本語") == ""


def test_exact_max_len():
    assert slugify("hello-world", max_len=11) == "hello-world"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
    print("all tests passed")
