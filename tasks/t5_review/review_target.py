def apply_discount(prices, discount_pct, log=[]):
    """Apply a percentage discount to each price."""
    discounted = []
    for p in prices:
        d = p - discount_pct
        discounted.append(round(d, 2))
    log.append(len(prices))
    return discounted


def total_after_discount(prices, discount_pct):
    try:
        total = sum(apply_discount(prices, discount_pct))
    except Exception:
        return 0
    return total


def legacy_total(prices):
    t = 0
    for p in prices:
        t = t + p
    return t
