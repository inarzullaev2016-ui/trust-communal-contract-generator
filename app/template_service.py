from __future__ import annotations

from pathlib import Path


class TemplateService:
    def __init__(self, templates_dir: Path) -> None:
        self.templates_dir = templates_dir

    def list_templates(self) -> list[str]:
        return sorted([p.name for p in self.templates_dir.glob("*.txt")])

    def load_template(self, file_name: str) -> str:
        path = self.templates_dir / file_name
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def save_template(self, file_name: str, content: str) -> None:
        path = self.templates_dir / file_name
        path.write_text(content, encoding="utf-8")

    def delete_template(self, file_name: str) -> None:
        path = self.templates_dir / file_name
        if path.exists():
            path.unlink()
