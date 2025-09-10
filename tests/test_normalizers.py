from __future__ import annotations

import pandas as pd

from medmentions.normalizers import normalize_drugs, normalize_pubmed, normalize_trials


def test_normalize_drugs_normalizes_text_and_trims_atccode():
    df = pd.DataFrame(
        {
            "atccode": ["  A04AD  ", "B01  "],
            "drug": ["  Café  ", "Hello\nWorld"],
            "other": [1, 2],
        }
    )

    out = normalize_drugs(df)

    assert list(out.columns) == ["atccode", "drug", "other"]
    # atccode kept as string and trimmed
    assert list(out["atccode"]) == ["A04AD", "B01"]
    # drug normalized (diacritics removed, lowercased, whitespace collapsed)
    assert list(out["drug"]) == ["cafe", "hello world"]
    # other column preserved
    assert list(out["other"]) == [1, 2]


def test_normalize_pubmed_normalizes_title_journal_and_parses_date():
    df = pd.DataFrame(
        {
            "id": ["1", "2"],
            "title": ["  Hello  World ", " Café\tau\tlait"],
            "journal": ["  The\nJournal  ", " Another\tJournal  "],
            "date": ["12 January 2023", "01/04/2024"],
        }
    )

    out = normalize_pubmed(df)

    assert list(out.columns) == ["id", "title", "journal", "date"]
    assert list(out["title"]) == ["hello world", "cafe au lait"]
    assert list(out["journal"]) == ["the journal", "another journal"]
    assert list(out["date"]) == [
        pd.Timestamp("2023-01-12").date(),
        pd.Timestamp("2024-04-01").date(),
    ]


def test_normalize_trials_normalizes_scientific_title_journal_and_parses_date():
    df = pd.DataFrame(
        {
            "id": ["t1", "t2"],
            "scientific_title": ["  Epinephrine Study ", "  Café  Study"],
            "journal": [" Clin\nTrials  ", "  J\tMed  "],
            "date": ["03-09-1999", "2023/01/12"],
        }
    )

    out = normalize_trials(df)

    assert list(out.columns) == ["id", "scientific_title", "journal", "date"]
    assert list(out["scientific_title"]) == ["epinephrine study", "cafe study"]
    assert list(out["journal"]) == ["clin trials", "j med"]
    assert list(out["date"]) == [
        pd.Timestamp("1999-09-03").date(),
        pd.Timestamp("2023-01-12").date(),
    ]
