from __future__ import annotations

from pathlib import Path

from app.paths import TEMPLATES_DIR


ALLOWED_TEMPLATE_SUFFIX = ".txt"


def _sanitize_template_name(name: str) -> str:
    cleaned = "".join(ch for ch in name.strip() if ch.isalnum() or ch in ("_", "-", " "))
    return cleaned.strip().replace(" ", "_")


def template_path(template_name: str) -> Path:
    safe_name = _sanitize_template_name(template_name)
    if not safe_name:
        raise ValueError("Название шаблона не может быть пустым")
    return TEMPLATES_DIR / f"{safe_name}{ALLOWED_TEMPLATE_SUFFIX}"


def list_templates() -> list[str]:
    items = sorted(TEMPLATES_DIR.glob(f"*{ALLOWED_TEMPLATE_SUFFIX}"))
    return [item.stem for item in items]


def read_template(template_name: str) -> str:
    path = template_path(template_name)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def save_template(template_name: str, body: str) -> str:
    path = template_path(template_name)
    path.write_text(body, encoding="utf-8")
    return path.stem


def delete_template(template_name: str) -> None:
    path = template_path(template_name)
    if path.exists():
        path.unlink()
