import pandas as pd

from medmentions.mentions import build_graph_df, compute_mentions, journal_with_most_distinct_drugs


def make_df(data, columns):
    return pd.DataFrame(data, columns=columns)


# ---------- compute_mentions ----------


def test_compute_mentions_basic_pubmed_and_clinical():
    drugs = make_df(
        [["A01", "Epinephrine"]],
        ["atccode", "drug"],
    )

    pubmed = make_df(
        [
            ["p1", "Study on Epinephrine response", "J1", "2020-02-01"],
            ["p2", "Unrelated title", "J2", "2020-02-02"],
        ],
        ["id", "title", "journal", "date"],
    )

    trials = make_df(
        [
            [
                "t1",
                "Clinical trial of epinephrine dosage",
                "J3",
                "2020-03-04",
            ],
            ["t2", "Another study", "J4", "2020-03-05"],
        ],
        ["id", "scientific_title", "journal", "date"],
    )

    out = compute_mentions(drugs, pubmed, trials)

    expected_cols = [
        "drug_atccode",
        "drug_name",
        "source_type",
        "source_id",
        "source_title",
        "journal",
        "date",
    ]
    assert list(out.columns) == expected_cols
    # One hit in pubmed (p1) and one in clinical (t1)
    assert len(out) == 2

    # PubMed row checks
    pm = out[out["source_type"] == "pubmed"].iloc[0]
    assert pm["drug_atccode"] == "A01"
    assert pm["drug_name"] == "Epinephrine"
    assert pm["source_id"] == "p1"
    assert pm["source_title"] == "Study on Epinephrine response"
    assert pm["journal"] == "J1"
    assert pm["date"] == "2020-02-01"

    # Clinical row checks
    cl = out[out["source_type"] == "clinical"].iloc[0]
    assert cl["drug_atccode"] == "A01"
    assert cl["drug_name"] == "Epinephrine"
    assert cl["source_id"] == "t1"
    assert cl["source_title"] == "Clinical trial of epinephrine dosage"
    assert cl["journal"] == "J3"
    assert cl["date"] == "2020-03-04"


def test_compute_mentions_case_insensitive_and_multi_hit():
    drugs = make_df([["D01", "Aspirin"], ["D02", "Paracetamol"]], ["atccode", "drug"])

    pubmed = make_df(
        [
            ["p1", "ASPIRIN reduces fever", "JX", "2021-01-01"],
            ["p2", "Effect of Paracetamol on pain", "JY", "2021-01-02"],
        ],
        ["id", "title", "journal", "date"],
    )

    trials = make_df(
        [
            [
                "t1",
                "Combined Aspirin and paracetamol study",
                "JZ",
                "2021-02-03",
            ]
        ],
        ["id", "scientific_title", "journal", "date"],
    )

    out = compute_mentions(drugs, pubmed, trials)

    # Expect 4 rows: 2 pubmed + 2 clinical (t1 matches both drugs)
    assert len(out) == 4

    # Validate counts per (drug, source_type)
    counts = out.groupby(["drug_name", "source_type"]).size().rename("n").reset_index()
    expected = {
        ("Aspirin", "pubmed"): 1,
        ("Paracetamol", "pubmed"): 1,
        ("Aspirin", "clinical"): 1,
        ("Paracetamol", "clinical"): 1,
    }
    for _, row in counts.iterrows():
        assert expected[(row["drug_name"], row["source_type"])] == row["n"]


def test_compute_mentions_handles_missing_titles_and_no_hits():
    drugs = make_df([["X01", "FooDrug"]], ["atccode", "drug"])
    pubmed = make_df([["p1", None, "J", "2020-01-01"]], ["id", "title", "journal", "date"])
    trials = make_df(
        [["t1", None, "J", "2020-01-02"]], ["id", "scientific_title", "journal", "date"]
    )

    out = compute_mentions(drugs, pubmed, trials)
    assert out.empty
    assert list(out.columns) == [
        "drug_atccode",
        "drug_name",
        "source_type",
        "source_id",
        "source_title",
        "journal",
        "date",
    ]


# ---------- build_graph_df ----------


def test_build_graph_df_structure_and_dates_normalization():
    edges = make_df(
        [
            [
                "A01",
                "Epinephrine",
                "pubmed",
                "p1",
                "Study on epinephrine",
                "J1",
                "2020-02-01",
            ],
            [
                "B02",
                "Aspirin",
                "clinical",
                "t1",
                "Clinical trial on aspirin",
                "J2",
                "2021-03-04",
            ],
        ],
        [
            "drug_atccode",
            "drug_name",
            "source_type",
            "source_id",
            "source_title",
            "journal",
            "date",
        ],
    )

    g = build_graph_df(edges)
    assert set(g.keys()) == {"drugs", "journals", "edges"}

    # drugs are sorted by code
    assert g["drugs"] == [
        {"atccode": "A01", "name": "Epinephrine"},
        {"atccode": "B02", "name": "Aspirin"},
    ]

    # journals sorted ascending and unique
    assert g["journals"] == ["J1", "J2"]

    # edges converted with date as YYYY-MM-DD strings
    assert len(g["edges"]) == 2
    assert g["edges"][0]["date"] == "2020-02-01"
    assert g["edges"][1]["date"] == "2021-03-04"


# ---------- journal_with_most_distinct_drugs ----------


def test_journal_with_most_distinct_drugs_empty():
    empty_edges = make_df(
        [],
        [
            "drug_atccode",
            "drug_name",
            "source_type",
            "source_id",
            "source_title",
            "journal",
            "date",
        ],
    )
    assert journal_with_most_distinct_drugs(empty_edges) == {
        "journal": None,
        "distinct_drugs": 0,
    }


def test_journal_with_most_distinct_drugs_basic():
    edges = make_df(
        [
            ["A01", "Epinephrine", "pubmed", "p1", "t1", "J1", "2020-01-01"],
            ["A01", "Epinephrine", "clinical", "t1", "t1", "J2", "2020-01-02"],
            ["B02", "Aspirin", "pubmed", "p2", "t2", "J1", "2020-01-03"],
            ["C03", "Paracetamol", "pubmed", "p3", "t3", "J3", "2020-01-04"],
        ],
        [
            "drug_atccode",
            "drug_name",
            "source_type",
            "source_id",
            "source_title",
            "journal",
            "date",
        ],
    )

    top = journal_with_most_distinct_drugs(edges)
    # J1 has two distinct drugs (A01, B02); others have 1
    assert top == {"journal": "J1", "distinct_drugs": 2}
