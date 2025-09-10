from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

import pandas as pd

# Add repo root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Path to mentions_edges.csv relative to this script: ../data/intermediary/mentions_edges.csv
MENTIONS_INTER = (
    Path(__file__).resolve().parent.parent / "data" / "intermediary" / "mentions_edges.csv"
)


def read_mentions_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).rename(columns=str.lower)

    # id, title, journal, date
    return df


def journal_with_most_distinct_drugs(edges: pd.DataFrame) -> Dict[str, Any]:
    if edges.empty:
        return {"journal": None, "distinct_drugs": 0}
    counts = edges.groupby("journal")["drug_atccode"].nunique().sort_values(ascending=False)
    top_journal = counts.index[0]
    return {"journal": top_journal, "distinct_drugs": int(counts.iloc[0])}


def main() -> None:
    mentions_edges = read_mentions_csv(MENTIONS_INTER)
    print(journal_with_most_distinct_drugs(mentions_edges))


if __name__ == "__main__":
    main()
