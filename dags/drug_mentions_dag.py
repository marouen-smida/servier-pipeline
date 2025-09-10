from __future__ import annotations

import os
import sys

import pandas as pd

# Add repo root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta
from pathlib import Path

from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor

from src.medmentions.intermediary_io import load_df_csv, save_df_csv
from src.medmentions.mentions import build_graph_df, compute_mentions
from src.medmentions.normalizers import normalize_drugs, normalize_pubmed, normalize_trials
from src.medmentions.readers import (
    read_clinical_trials_csv,
    read_drugs_csv,
    read_pubmed_csv,
    read_pubmed_json,
)
from src.medmentions.writers import write_graph

DATA_DIR = Path(os.environ.get("PIPELINE_DATA_DIR", "/usr/local/airflow/include"))
INTER_DIR = Path(os.environ.get("PIPELINE_INTER_DIR", "/usr/local/airflow/data/intermediary"))
OUT_DIR = Path(os.environ.get("PIPELINE_PROCESSED_DIR", "/usr/local/airflow/data/processed"))


OUT_JSON = OUT_DIR / "graph.json"
DRUGS_INTER = INTER_DIR / "drugs_normalized.csv"
PUBMED_INTER = INTER_DIR / "pubmed_normalized.csv"
TRIALS_INTER = INTER_DIR / "trials_normalized.csv"
MENTIONS_INTER = INTER_DIR / "mentions_edges.csv"
TOP_JOURNAL_JSON = INTER_DIR / "top_journal.json"

default_args = {
    "owner": "servier",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="servier_pipeline",
    description="Build drug-mention graph from PubMed + clinical trials (pandas)",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # modern style; equivalent to schedule_interval=None
    catchup=False,
    default_args=default_args,
    tags=["servier", "pipeline", "pandas"],
)
def drug_mentions_dag():

    # --- Sensors (operators), not @task-wrapped ---
    wait_drugs = FileSensor(
        task_id="wait_drugs_csv",
        filepath=str(DATA_DIR / "drugs.csv"),
        poke_interval=60,
        mode="reschedule",
        timeout=6 * 60 * 60,
    )

    wait_pubmed_csv = FileSensor(
        task_id="wait_pubmed_csv",
        filepath=str(DATA_DIR / "pubmed.csv"),
        poke_interval=60,
        mode="reschedule",
        timeout=6 * 60 * 60,
    )

    wait_pubmed_json = FileSensor(
        task_id="wait_pubmed_json",
        filepath=str(DATA_DIR / "pubmed.json"),
        poke_interval=60,
        mode="reschedule",
        timeout=6 * 60 * 60,
    )

    wait_trials = FileSensor(
        task_id="wait_clinical_trials_csv",
        filepath=str(DATA_DIR / "clinical_trials.csv"),
        poke_interval=60,
        mode="reschedule",
        timeout=6 * 60 * 60,
    )

    # --- TaskFlow tasks ---
    @task(task_id="read_and_normalize_to_csv")
    def read_and_normalize_to_csv():
        # Read
        drugs = read_drugs_csv(DATA_DIR / "drugs.csv")
        pubmed = pd.concat(
            [
                read_pubmed_csv(DATA_DIR / "pubmed.csv"),
                read_pubmed_json(DATA_DIR / "pubmed.json"),
            ],
            ignore_index=True,
        )
        trials = read_clinical_trials_csv(DATA_DIR / "clinical_trials.csv")

        # Normalize
        drugs_n = normalize_drugs(drugs)
        pubmed_n = normalize_pubmed(pubmed)
        trials_n = normalize_trials(trials)

        # Persist intermediates (ensure dirs exist)
        DRUGS_INTER.parent.mkdir(parents=True, exist_ok=True)
        PUBMED_INTER.parent.mkdir(parents=True, exist_ok=True)
        TRIALS_INTER.parent.mkdir(parents=True, exist_ok=True)

        save_df_csv(drugs_n, DRUGS_INTER)
        save_df_csv(pubmed_n, PUBMED_INTER)
        save_df_csv(trials_n, TRIALS_INTER)

    @task(task_id="compute_mentions_and_write_outputs")
    def compute_mentions_and_write_outputs():
        # Load intermediates
        drugs_n = load_df_csv(DRUGS_INTER)
        pubmed_n = load_df_csv(PUBMED_INTER)
        trials_n = load_df_csv(TRIALS_INTER)

        # Mentions
        mentions = compute_mentions(drugs_n, pubmed_n, trials_n)
        save_df_csv(mentions, MENTIONS_INTER)

        # Graph + top journal
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        INTER_DIR.mkdir(parents=True, exist_ok=True)

        graph = build_graph_df(mentions)
        write_graph(graph, OUT_JSON)

    rn = read_and_normalize_to_csv()
    cw = compute_mentions_and_write_outputs()

    # Dependencies: all sensors -> rn -> cw
    [wait_drugs, wait_pubmed_csv, wait_pubmed_json, wait_trials] >> rn >> cw


dag = drug_mentions_dag()
