import re
import unicodedata


def slugify(text, max_len=50):
    # NFKD splits accented chars into base + combining marks; the ASCII
    # encode then drops the marks and any other non-ASCII, leaving "creme".
    ascii_text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")

    if len(slug) <= max_len:
        return slug

    # Keep the longest run of whole words that fits in max_len.
    words = slug.split("-")
    result = ""
    for word in words:
        candidate = word if not result else result + "-" + word
        if len(candidate) > max_len:
            break
        result = candidate

    # Empty means even the first word overflows: hard-truncate it.
    return result or words[0][:max_len]
