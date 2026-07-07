import re
import unicodedata


def slugify(text, max_len=50):
    # NFKD-normalize, then drop anything that doesn't map to ASCII.
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    if len(slug) <= max_len:
        return slug
    if slug[max_len] == "-":
        # Cut lands exactly on a word boundary; the last word is complete.
        return slug[:max_len]
    cut = slug[:max_len]
    idx = cut.rfind("-")
    if idx == -1:
        # First word alone exceeds max_len: hard-truncate it.
        return cut
    return cut[:idx]
