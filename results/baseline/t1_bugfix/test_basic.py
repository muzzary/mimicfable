from intervals import merge_intervals


def test_simple_overlap():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


if __name__ == "__main__":
    test_simple_overlap()
    print("basic test passed")
