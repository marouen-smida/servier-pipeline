import pytest

from medmentions.utils import normalize_text


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
