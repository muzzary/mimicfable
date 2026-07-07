# Bug report

Customers using discount codes are being undercharged. Per policy (and the docstring),
discounts apply to ITEMS ONLY, but `compute_total` in `orders.py` currently applies the
discount to shipping as well.

Example: items worth 20.00 with code SAVE10 and 5.00 shipping should total
20.00 * 0.9 + 5.00 = 23.00. The code currently returns 22.50.

## Deliverable

Fix this bug.
