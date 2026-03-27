from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(file_path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not file_path.exists():
        return default.copy() if default else {}
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path: Path, payload: dict[str, Any]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
