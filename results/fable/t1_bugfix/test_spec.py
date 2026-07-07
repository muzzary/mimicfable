from intervals import merge_intervals


def test_touching_intervals_merge():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_unsorted_input_sorted_output():
    assert merge_intervals([[4, 5], [1, 2]]) == [[1, 2], [4, 5]]
    assert merge_intervals([[2, 6], [1, 3]]) == [[1, 6]]


def test_no_overlap_preserved():
    assert merge_intervals([[1, 2], [3, 4], [5, 6]]) == [[1, 2], [3, 4], [5, 6]]


def test_input_not_mutated():
    outer = [[2, 6], [1, 3]]
    inner_snapshot = [list(iv) for iv in outer]
    merge_intervals(outer)
    assert outer == inner_snapshot
    assert [id(iv) for iv in outer]  # inner lists still present, unchanged
    assert outer[0] == [2, 6] and outer[1] == [1, 3]


def test_empty_input():
    assert merge_intervals([]) == []


def test_nested_containment():
    assert merge_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("spec tests passed")
