import re
import unicodedata


def slugify(text, max_len=50):
    # NFKD-normalize, then drop any character that isn't plain ASCII.
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()

    # Collapse every run of non-alphanumeric ASCII into a single hyphen,
    # then drop any leading/trailing hyphens.
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    if not slug:
        return ""

    if len(slug) <= max_len:
        return slug

    # Too long: cut at max_len, then trim back to the last complete word.
    # If the character right at the boundary is a hyphen, slug[:max_len]
    # already ends on a word boundary; otherwise we sliced mid-word, so
    # drop the partial trailing word. When the first word alone exceeds
    # max_len there is no hyphen to split on, so this naturally leaves the
    # first word hard-truncated to max_len characters.
    truncated = slug[:max_len]
    if slug[max_len] != "-":
        truncated = truncated.rsplit("-", 1)[0]
    return truncated.strip("-")
