from __future__ import annotations
import unicodedata
import pandas as pd

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


def normalize_text_series(series: pd.Series) -> pd.Series:
    """Normalize a pandas Series of text using ``normalize_text``.

    - Preserves NaN values
    - Converts non-string values to string before normalizing

    Args:
        series: A pandas Series containing text values.

    Returns:
        A new pandas Series with normalized text.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("normalize_text_series expects a pandas Series")

    normalize_text_serie = series.copy()
    notna = normalize_text_serie.notna()
    # Normalize only non-NA entries; cast to str before normalization
    normalize_text_serie.loc[notna] = normalize_text_serie.loc[notna].astype(str).map(normalize_text)
    return normalize_text_serie

