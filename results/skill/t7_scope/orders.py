DISCOUNT_CODES = {"SAVE10": 0.10, "SAVE20": 0.20}


def compute_total(items, code=None, shipping=5.0):
    """Total = discounted items + shipping. Discounts apply to items only."""
    subtotal = 0
    for price, qty in items:
        subtotal = subtotal + price * qty
    if code in DISCOUNT_CODES:
        subtotal = subtotal * (1 - DISCOUNT_CODES[code])
    total = subtotal + shipping
    return round(total, 2)


def order_summary(items, code=None):
    lines = []
    for price, qty in items:
        lines.append(f"{qty} x {price}")
    lines.append(f"total: {compute_total(items, code)}")
    return "\n".join(lines)


def legacy_summary(items):
    text = ""
    for price, qty in items:
        text = text + str(qty) + " x " + str(price) + "\n"
    return text
