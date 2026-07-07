def mean_of_list(numbers):
    numbers = list(numbers)
    if not numbers:
        raise ValueError("cannot compute mean of empty input")
    return sum(numbers) / len(numbers)


def mean_of_positive(numbers):
    return mean_of_list([n for n in numbers if n > 0])


def mean_of_negative(numbers):
    return mean_of_list([n for n in numbers if n < 0])


def variance(numbers):
    m = mean_of_list(numbers)
    return mean_of_list([(n - m) ** 2 for n in numbers])
