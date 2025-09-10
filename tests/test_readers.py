from pathlib import Path

from medmentions.readers import (
    read_clinical_trials_csv,
    read_drugs_csv,
    read_pubmed_csv,
    read_pubmed_json,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "include" / "raw"


def print_all_dataframes() -> None:
    """Utility to read all source files and print the resulting DataFrames."""
    drugs_df = read_drugs_csv(DATA_DIR / "drugs.csv")
    pubmed_csv_df = read_pubmed_csv(DATA_DIR / "pubmed.csv")
    pubmed_json_df = read_pubmed_json(DATA_DIR / "pubmed.json")
    trials_df = read_clinical_trials_csv(DATA_DIR / "clinical_trials.csv")

    print("=== drugs.csv ===")
    print(drugs_df)
    print("\n=== pubmed.csv ===")
    print(pubmed_csv_df)
    print("\n=== pubmed.json ===")
    print(pubmed_json_df)
    print("\n=== clinical_trials.csv ===")
    print(trials_df)


def test_read_drugs_csv_reads_expected_columns_and_rows():
    df = read_drugs_csv(DATA_DIR / "drugs.csv")
    assert list(df.columns) == ["atccode", "drug"]
    # known sample entries
    assert not df.empty
    assert (df["atccode"] == "A04AD").any()
    assert (df["drug"].str.upper() == "DIPHENHYDRAMINE").any()


def test_read_pubmed_csv_columns_and_date_as_str():
    df = read_pubmed_csv(DATA_DIR / "pubmed.csv")
    assert list(df.columns) == ["id", "title", "journal", "date"]
    # Ensure date is kept as string by the reader (dtype=str)
    assert df["date"].dtype == object
    assert "01/01/2019" in set(df["date"]) or "2019-01-01" in set(df["date"])  # mixed in file


def test_read_pubmed_json_handles_trailing_commas_and_columns():
    df = read_pubmed_json(DATA_DIR / "pubmed.json")
    assert list(df.columns) == ["id", "title", "journal", "date"]
    # id column should be string due to dtype=str downstream expectations
    assert df["id"].dtype == object
    # contains an entry mentioning isoprenaline
    assert df["title"].str.contains("isoprenaline", case=False).any()


def test_read_clinical_trials_csv_columns_and_sample_rows():
    df = read_clinical_trials_csv(DATA_DIR / "clinical_trials.csv")
    assert list(df.columns) == ["id", "scientific_title", "journal", "date"]
    assert not df.empty
    # Contains an epinephrine related trial
    assert df["scientific_title"].str.contains("Epinephrine", case=False, na=False).any()


def test_print_all_dataframes_smoke():
    """Smoke test to ensure print utility runs without errors.

    Run `pytest -s -k print_all_dataframes_smoke` to see printed DataFrames.
    """
    print_all_dataframes()
