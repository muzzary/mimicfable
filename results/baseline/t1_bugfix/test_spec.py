from intervals import merge_intervals


def test_overlap():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


def test_touching_merges():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_any_order_sorted_output():
    assert merge_intervals([[8, 10], [1, 3], [2, 6], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_no_mutation():
    inp = [[1, 3], [2, 6]]
    inner = inp[0]
    snapshot = [list(x) for x in inp]
    merge_intervals(inp)
    assert inp == snapshot
    assert inner == [1, 3]  # same object must be unchanged


def test_empty():
    assert merge_intervals([]) == []


def test_disjoint_unchanged():
    assert merge_intervals([[1, 2], [5, 6]]) == [[1, 2], [5, 6]]


def test_nested_interval():
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("all spec tests passed")
