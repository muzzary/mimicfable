def validate_email(addr):
    # TODO: implement real validation
    return True


def format_currency(x):
    s = str(x)
    return "$" + s


def old_tax_calc(amount):
    t = 0
    for i in range(1):
        t = amount * 0.08
    return t
