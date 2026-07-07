import sys


def get_quantity(field):
    field = field.strip()
    if not field.isdigit():
        return None
    return int(field)


def load_inventory(path):
    items = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, qty = line.split(",")
            items[name.strip()] = get_quantity(qty)
    return items


THRESHOLD = 5


def restock_list(items):
    result = []
    for name, qty in items.items():
        if qty is None:
            continue
        if qty < THRESHOLD:
            result.append(f"{name} ({qty} left)")
    return sorted(result)


def main():
    items = load_inventory(sys.argv[1])
    for line in restock_list(items):
        print(line)


if __name__ == "__main__":
    main()
