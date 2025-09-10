import pandas as pd
import pytest

from medmentions.utils import normalize_dates, normalize_text, normalize_text_series


# ---------- normalize_text ----------
@pytest.mark.parametrize(
    "raw,expected",
    [
        ("  Hello  World  ", "hello world"),
        ("Hello\t\tWorld", "hello world"),
        ("Hello\nWorld", "hello world"),
        ("\u00A0Hello\u00A0World\u00A0", "hello world"),  # NBSP handling
        (" Café\u00A0au\u00A0lait ", "cafe au lait"),  # accents removed
    ],
)
def test_normalize_text(raw, expected):
    assert normalize_text(raw) == expected


# ---------- normalize_text_series ----------
def test_normalize_text_series_basic():
    s = pd.Series(["  Café  ", "Hello\nWorld", None, 123])
    out = normalize_text_series(s)
    assert list(out) == ["cafe", "hello world", None, "123"]


def test_normalize_text_series_preserves_nan():
    s = pd.Series([None, float("nan"), "  A  "])
    out = normalize_text_series(s)
    assert pd.isna(out.iloc[1])
    assert out.iloc[0] is None
    assert out.iloc[2] == "a"


# ---------- normalize_dates (date objects) ----------
def test_normalize_dates_objects():
    s = pd.Series(
        [
            "12 January 2023",
            "12 Jan 2023",
            "01/04/2024",
            "03-09-1999",
            "2023-01-12",
            "2023/01/12",
        ]
    )
    out = normalize_dates(s)
    assert list(out) == [
        pd.Timestamp("2023-01-12").date(),
        pd.Timestamp("2023-01-12").date(),
        pd.Timestamp("2024-04-01").date(),
        pd.Timestamp("1999-09-03").date(),
        pd.Timestamp("2023-01-12").date(),
        pd.Timestamp("2023-01-12").date(),
    ]
