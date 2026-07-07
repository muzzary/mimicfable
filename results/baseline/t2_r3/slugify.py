import re
import unicodedata


def slugify(text, max_len=50):
    # NFKD-normalize, drop non-ASCII, lowercase.
    ascii_text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    # Collapse every run of non-alphanumerics to a single hyphen; no edge hyphens.
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")

    if not slug or len(slug) <= max_len:
        return slug

    # First word alone too long -> hard-truncate it.
    first_word = slug.split("-", 1)[0]
    if len(first_word) > max_len:
        return first_word[:max_len]

    # Cut at max_len; if we landed on a word boundary keep it, else drop the
    # partial trailing word so we never end mid-word or on a hyphen.
    if slug[max_len] == "-":
        return slug[:max_len]
    return slug[:max_len].rsplit("-", 1)[0]
