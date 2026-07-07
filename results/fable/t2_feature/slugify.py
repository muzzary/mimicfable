import re
import unicodedata


def slugify(text, max_len=50):
    # NFKD + ASCII-only drops accents (Crème -> Creme) by stripping the
    # combining marks that decomposition separates out.
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")

    if len(slug) <= max_len:
        return slug

    truncated = slug[:max_len]
    # slug[max_len] is the char just past the cut. If it isn't a boundary
    # hyphen, the cut landed mid-word, so drop that partial trailing word.
    if slug[max_len] != "-" and "-" in truncated:
        truncated = truncated[: truncated.rindex("-")]
    # No hyphen to fall back to means the first word alone exceeds max_len:
    # keep the hard truncation. Otherwise clean any dangling hyphen.
    return truncated.rstrip("-")
