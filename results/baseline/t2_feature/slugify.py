import re
import unicodedata


def slugify(text, max_len=50):
    """Convert text to a URL slug (see README.md for the exact spec)."""
    # 1. NFKD-normalize and drop non-ASCII characters.
    ascii_text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    # 2-4. Lowercase, collapse non-alphanumeric runs to a single hyphen, trim ends.
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")

    # 6. Nothing left.
    if not slug:
        return ""

    # 5. Length limit.
    if len(slug) <= max_len:
        return slug

    first_word = slug.split("-", 1)[0]
    if len(first_word) > max_len:
        # First word alone is too long: hard-truncate it.
        return first_word[:max_len]

    cut = slug[:max_len]
    if slug[max_len] != "-":
        # The cut landed mid-word; trim back to the last complete word.
        cut = cut.rsplit("-", 1)[0]
    return cut
