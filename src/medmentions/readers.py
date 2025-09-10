from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


def read_drugs_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).rename(columns=str.lower)
    # Expected columns: atccode, drug
    return df[["atccode", "drug"]]


def read_pubmed_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).rename(columns=str.lower)

    # id, title, journal, date
    return df[["id", "title", "journal", "date"]]


def read_pubmed_json(path: str | Path) -> pd.DataFrame:
    # Be tolerant to trailing commas in the JSON (present in the sample file)
    text = Path(path).read_text(encoding="utf-8")
    # Remove trailing commas before closing braces/brackets: ", }" or ", ]"
    cleaned = re.sub(r",\s*([}\]])", r"\1", text)
    data = json.loads(cleaned)
    df = pd.DataFrame(data).rename(columns=str.lower)
    return df[["id", "title", "journal", "date"]]


def read_clinical_trials_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).rename(columns=str.lower)
    # id, scientific_title, journal, date
    return df[["id", "scientific_title", "journal", "date"]]
