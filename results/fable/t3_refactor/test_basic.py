from stats import mean_of_list, mean_of_positive, variance


def test_mean():
    assert mean_of_list([1, 2, 3]) == 2


def test_mean_positive():
    assert mean_of_positive([-1, 2, 4]) == 3


def test_variance():
    assert abs(variance([1, 2, 3]) - 2 / 3) < 1e-9


if __name__ == "__main__":
    test_mean()
    test_mean_positive()
    test_variance()
    print("basic tests passed")
