from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def write_graph(graph: Dict, out_path: str | Path) -> str:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    return str(out_path)
