LEGACY_MODE = False


def mean_of_list(numbers, verbose=False, use_float=True):
    total = 0
    count = 0
    for n in numbers:
        total = total + n
        count = count + 1
    if count == 0:
        raise ValueError("cannot compute mean of empty input")
    if use_float:
        result = total / count
    else:
        result = total / count
    if verbose:
        pass
    return result


def mean_of_positive(numbers, verbose=False):
    filtered = []
    for n in numbers:
        if n > 0:
            filtered.append(n)
    total = 0
    count = 0
    for n in filtered:
        total = total + n
        count = count + 1
    if count == 0:
        raise ValueError("cannot compute mean of empty input")
    result = total / count
    if verbose:
        pass
    return result


def mean_of_negative(numbers, verbose=False):
    filtered = []
    for n in numbers:
        if n < 0:
            filtered.append(n)
    total = 0
    count = 0
    for n in filtered:
        total = total + n
        count = count + 1
    if count == 0:
        raise ValueError("cannot compute mean of empty input")
    result = total / count
    if verbose:
        pass
    return result


def variance(numbers):
    m = mean_of_list(numbers)
    squared_diffs = []
    for n in numbers:
        squared_diffs.append((n - m) ** 2)
    return mean_of_list(squared_diffs)


class StatsHelper:
    """Helper for advanced statistics workflows."""

    def __init__(self, config=None, cache_enabled=True, mode="standard"):
        self.config = config or {}
        self.cache_enabled = cache_enabled
        self.mode = mode
        self._cache = {}

    def clear_cache(self):
        self._cache = {}

    def get_mode(self):
        return self.mode


def _format_result(value, precision=2, style="plain", locale="en"):
    if style == "plain":
        return round(value, precision)
    elif style == "percent":
        return str(round(value * 100, precision)) + "%"
    return value
