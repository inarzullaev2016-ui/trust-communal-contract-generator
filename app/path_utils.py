from __future__ import annotations

from pathlib import Path
import sys


def get_app_root() -> Path:
    """Return root folder for both Python run and bundled exe run."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def ensure_project_dirs(root: Path) -> dict[str, Path]:
    dirs = {
        "templates": root / "templates",
        "data": root / "data",
        "generated": root / "generated",
        "settings": root / "settings",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs
