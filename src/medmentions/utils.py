from __future__ import annotations

import unicodedata
from datetime import date
from typing import Any

import pandas as pd

# Data formats that needs to be normalized
_DATE_FORMATS = [
    "%d %B %Y",  # 12 January 2023
    "%d %b %Y",  # 12 Jan 2023
    "%d/%m/%Y",  # 01/04/2024
    "%d-%m-%Y",  # 03-09-1999
    "%Y-%m-%d",  # 2023-01-12
    "%Y/%m/%d",  # 2023/01/12
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


def normalize_text_series(series: pd.Series[Any]) -> pd.Series[Any]:
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

    # Build a normalized object series while preserving None/NaN as-is
    values: list[Any] = []
    for x in series:
        if pd.isna(x):  # preserves None, NaN, pd.NA
            values.append(x)
        else:
            values.append(normalize_text(str(x)))

    return pd.Series(values, index=series.index, dtype="object")


def normalize_dates(series: pd.Series[Any]) -> pd.Series[date]:
    """
    Normalize a pandas Series of date-like strings into Python ``date`` objects.

    This function attempts to parse each value in the Series into a date using
    a predefined set of formats (``_DATE_FORMATS``). If none of the formats
    match, it falls back to pandas' automatic date inference. If parsing fails
    for any values, a ``ValueError`` is raised listing the problematic entries.

    Parameters
    ----------
    series : pd.Series
        Input pandas Series containing strings (or values convertible to strings)
        representing dates.

    Returns
    -------
    pd.Series
        A Series of Python ``datetime.date`` objects with the same index as the
        input Series.

    Raises
    ------
    ValueError
        If some values cannot be parsed into valid dates.

    Notes
    -----
    - Leading and trailing whitespace is stripped from all input values.
    - Parsing tries formats in ``_DATE_FORMATS`` first, then falls back to
      pandas' automatic inference.
    - Parsing assumes ``dayfirst=True`` (i.e., "01-02-2023" → 1 Feb 2023).
    """
    s = series.astype(str).str.strip()
    parsed = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    mask = pd.Series(True, index=s.index)

    for fmt in _DATE_FORMATS:
        part = pd.to_datetime(s[mask], format=fmt, errors="coerce", dayfirst=True)
        fill = part.notna()
        parsed.loc[fill.index[fill]] = part[fill]
        mask &= ~fill

    # Fallback: let pandas infer
    if mask.any():
        part = pd.to_datetime(
            s[mask], errors="coerce", dayfirst=True, infer_datetime_format=True
        )
        fill = part.notna()
        parsed.loc[fill.index[fill]] = part[fill]
        mask &= ~fill

    if parsed.isna().any():
        bad = s[parsed.isna()].unique().tolist()
        raise ValueError(
            f"Unrecognized date formats: {bad[:5]}{'...' if len(bad) > 5 else ''}"
        )

    return parsed.dt.date
