def _mean(numbers):
    numbers = list(numbers)
    if not numbers:
        raise ValueError("cannot compute mean of empty input")
    return sum(numbers) / len(numbers)


def mean_of_list(numbers):
    return _mean(numbers)


def mean_of_positive(numbers):
    return _mean([n for n in numbers if n > 0])


def mean_of_negative(numbers):
    return _mean([n for n in numbers if n < 0])


def variance(numbers):
    m = mean_of_list(numbers)
    return _mean([(n - m) ** 2 for n in numbers])
