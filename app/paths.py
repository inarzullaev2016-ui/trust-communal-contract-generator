from __future__ import annotations

from pathlib import Path
import sys


def app_root() -> Path:
    """Return directory where executable/script is located."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


ROOT_DIR = app_root()
TEMPLATES_DIR = ROOT_DIR / "templates"
DATA_DIR = ROOT_DIR / "data"
GENERATED_DIR = ROOT_DIR / "generated"
SETTINGS_DIR = ROOT_DIR / "settings"
LANDLORD_FILE = SETTINGS_DIR / "landlord_details.json"


def ensure_runtime_dirs() -> None:
    for path in (TEMPLATES_DIR, DATA_DIR, GENERATED_DIR, SETTINGS_DIR):
        path.mkdir(parents=True, exist_ok=True)
