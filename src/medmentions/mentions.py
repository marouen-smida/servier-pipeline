import pandas as pd


def compute_mentions(
    drugs: pd.DataFrame, pubmed: pd.DataFrame, trials: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a DataFrame with columns:
    [drug_atccode, drug_name, source_type, source_id, source_title, journal, date]
    """
    edges = []

    # PubMed: match on title
    for _, d in drugs.iterrows():
        hits = pubmed[pubmed["title"].str.contains(d["drug"], case=False, na=False)]
        if not hits.empty:
            tmp = hits.assign(
                drug_atccode=d["atccode"],
                drug_name=d["drug"],
                source_type="pubmed",
                source_id=hits["id"],
                source_title=hits["title"],
            )[
                [
                    "drug_atccode",
                    "drug_name",
                    "source_type",
                    "source_id",
                    "source_title",
                    "journal",
                    "date",
                ]
            ]
            edges.append(tmp)

    # Clinical trials: match on scientific_title
    for _, d in drugs.iterrows():
        hits = trials[trials["scientific_title"].str.contains(d["drug"], case=False, na=False)]
        if not hits.empty:
            tmp = hits.assign(
                drug_atccode=d["atccode"],
                drug_name=d["drug"],
                source_type="clinical",
                source_id=hits["id"],
                source_title=hits["scientific_title"],
            )[
                [
                    "drug_atccode",
                    "drug_name",
                    "source_type",
                    "source_id",
                    "source_title",
                    "journal",
                    "date",
                ]
            ]
            edges.append(tmp)

    if len(edges) == 0:
        return pd.DataFrame(
            columns=[
                "drug_atccode",
                "drug_name",
                "source_type",
                "source_id",
                "source_title",
                "journal",
                "date",
            ]
        )

    return pd.concat(edges, ignore_index=True)


def build_graph_df(edges: pd.DataFrame) -> dict:
    drugs = edges[["drug_atccode", "drug_name"]].drop_duplicates().sort_values("drug_atccode")
    journals = sorted(edges["journal"].dropna().unique().tolist())
    out_edges = edges.copy()
    out_edges["date"] = pd.to_datetime(out_edges["date"]).dt.date.astype(str)

    return {
        "drugs": [
            {"atccode": r.drug_atccode, "name": r.drug_name} for r in drugs.itertuples(index=False)
        ],
        "journals": journals,
        "edges": out_edges.to_dict(orient="records"),
    }


def journal_with_most_distinct_drugs(edges: pd.DataFrame) -> dict:
    if edges.empty:
        return {"journal": None, "distinct_drugs": 0}
    counts = edges.groupby("journal")["drug_atccode"].nunique().sort_values(ascending=False)
    top_journal = counts.index[0]
    return {"journal": top_journal, "distinct_drugs": int(counts.iloc[0])}
