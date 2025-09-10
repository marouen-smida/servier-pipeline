from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def save_json(obj: Any, path: str | Path) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return str(path)


def save_df_csv(df: pd.DataFrame, path: str | Path) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return str(path)


def load_df_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)
