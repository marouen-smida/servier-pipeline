from __future__ import annotations
import unicodedata

#Data formats that needs to be normalized
_DATE_FORMATS = [
    "%d %B %Y",   # 12 January 2023
    "%d %b %Y",   # 12 Jan 2023
    "%d/%m/%Y",   # 01/04/2024
    "%d-%m-%Y",   # 03-09-1999
    "%Y-%m-%d",   # 2023-01-12
    "%Y/%m/%d",   # 2023/01/12
]


def normalize_text(text: str) -> str:
    """Return a simplified normalized string.

    Steps:
    - Remove accents/diacritics
    - Lowercase
    - Collapse multiple whitespace to a single space and trim
    """

    # Remove accents/diacritics via NFKD then drop combining marks
    decomposed = unicodedata.normalize("NFKD", text)
    no_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))

    # Lowercase
    lowered = no_accents.lower()

    # Collapse whitespace (tabs/newlines/NBSP) and trim
    collapsed = " ".join(lowered.split())
    return collapsed

