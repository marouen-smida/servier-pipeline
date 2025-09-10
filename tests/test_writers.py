from __future__ import annotations

import json
from pathlib import Path

from medmentions.writers import write_graph


def test_write_graph_creates_parent_and_writes_json(tmp_path: Path):
    # Arrange
    out_file = tmp_path / "nested" / "graph.json"
    graph = {
        "nodes": [
            {"id": 1, "label": "café"},  # non-ascii to ensure ensure_ascii=False
            {"id": 2, "label": "aspirin"},
        ],
        "edges": [{"source": 1, "target": 2, "type": "mentions"}],
    }

    # Act
    returned = write_graph(graph, out_file)

    # Assert: path returned and file exists
    assert returned == str(out_file)
    assert out_file.exists()

    # Assert: JSON content matches the original dict
    with out_file.open("r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == graph


def test_write_graph_accepts_str_path(tmp_path: Path):
    out_file = tmp_path / "graph.json"
    graph = {"hello": "world", "n": 3}

    returned = write_graph(graph, str(out_file))

    assert returned == str(out_file)
    assert out_file.is_file()
    assert json.loads(out_file.read_text(encoding="utf-8")) == graph
