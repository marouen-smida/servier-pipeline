from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pandas.testing as pdt

from medmentions.intermediary_io import load_df_csv, save_df_csv, save_json


def test_save_json_creates_parent_and_writes_json(tmp_path: Path):
    out_file = tmp_path / "nested" / "data.json"
    obj = {
        "greeting": "café",
        "n": 3,
        "items": [1, 2, 3],
    }

    returned = save_json(obj, out_file)

    assert returned == str(out_file)
    assert out_file.exists()
    with out_file.open("r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == obj


def test_save_and_load_df_csv_roundtrip(tmp_path: Path):
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "café"],
            "score": [10.5, 20.0, 30.25],
        }
    )

    out_file = tmp_path / "dir" / "table.csv"
    returned = save_df_csv(df, out_file)

    assert returned == str(out_file)
    assert out_file.is_file()

    loaded = load_df_csv(out_file)
    pdt.assert_frame_equal(loaded, df)
