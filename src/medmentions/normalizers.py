from __future__ import annotations

import pandas as pd

from .utils import normalize_dates, normalize_text_series


def normalize_drugs(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the drugs dataframe.

    - Normalize text in the ``drug`` column
    - Trim whitespace in ``atccode`` (kept as string)
    """
    out = df.copy()
    if "drug" in out.columns:
        out["drug"] = normalize_text_series(out["drug"])
    if "atccode" in out.columns:
        out["atccode"] = out["atccode"].astype(str).str.strip()
    return out


def normalize_pubmed(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the pubmed dataframe.

    - Normalize text in ``title`` and ``journal``
    - If present, parse ``date`` into ``datetime.date`` objects
    """
    out = df.copy()
    if "title" in out.columns:
        out["title"] = normalize_text_series(out["title"])
    if "journal" in out.columns:
        out["journal"] = normalize_text_series(out["journal"])
    if "date" in out.columns:
        out["date"] = normalize_dates(out["date"])
    return out


def normalize_trials(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the clinical trials dataframe.

    - Normalize text in ``scientific_title`` and ``journal``
    - If present, parse ``date`` into ``datetime.date`` objects
    """
    out = df.copy()
    if "scientific_title" in out.columns:
        out["scientific_title"] = normalize_text_series(out["scientific_title"])
    if "journal" in out.columns:
        out["journal"] = normalize_text_series(out["journal"])
    if "date" in out.columns:
        out["date"] = normalize_dates(out["date"])
    return out
