import pandas as pd

from medmentions.utils import normalize_text_series


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
