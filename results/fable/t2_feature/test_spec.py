from slugify import slugify


def test_readme_examples():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("the quick brown fox", max_len=12) == "the-quick"
    assert slugify("!!!") == ""


def test_unicode_dropped():
    assert slugify("Crème brûlée") == "creme-brulee"


def test_lowercase():
    assert slugify("ABC") == "abc"


def test_symbol_runs_collapse():
    assert slugify("Python 3.13") == "python-3-13"
    assert slugify("a---b___c") == "a-b-c"


def test_no_edge_hyphens():
    assert slugify("  leading and trailing  ") == "leading-and-trailing"
    assert slugify("...hi...") == "hi"


def test_truncate_trims_to_word():
    # cut lands mid "brown" -> trim back to "the-quick"
    assert slugify("the quick brown fox", max_len=12) == "the-quick"
    # cut lands exactly on a boundary hyphen -> keep whole words
    assert slugify("the quick brown", max_len=9) == "the-quick"


def test_first_word_hard_truncate():
    assert slugify("supercalifragilistic", max_len=5) == "super"
    # long first word followed by more: still hard-truncate the first word
    assert slugify("supercalifragilistic expialidocious", max_len=5) == "super"


def test_empty_and_symbols_only():
    assert slugify("") == ""
    assert slugify("@#$%") == ""


def test_no_truncation_when_short():
    assert slugify("short", max_len=50) == "short"
    # exactly at the limit is kept whole
    assert slugify("abcde", max_len=5) == "abcde"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name} passed")
    print("all spec tests passed")
