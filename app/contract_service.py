from __future__ import annotations

from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
import zipfile

from app.amount_words import rubles_to_words


CONTENT_TYPES_XML = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">
  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>
  <Default Extension=\"xml\" ContentType=\"application/xml\"/>
  <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>
</Types>
"""

RELS_XML = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">
  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>
</Relationships>
"""

DOC_RELS_XML = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"/>
"""


def _build_document_xml(text: str) -> str:
    paragraphs = []
    lines = text.splitlines() or [""]
    for line in lines:
        safe_line = escape(line)
        paragraphs.append(
            "<w:p><w:r><w:t xml:space=\"preserve\">"
            f"{safe_line}"
            "</w:t></w:r></w:p>"
        )

    body = "".join(paragraphs)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
        f"<w:body>{body}<w:sectPr/></w:body></w:document>"
    )


class ContractService:
    def __init__(self, generated_dir: Path) -> None:
        self.generated_dir = generated_dir

    def render_template(self, template_text: str, values: dict[str, str]) -> str:
        values = values.copy()
        if values.get("rent_amount"):
            values["rent_amount_words"] = rubles_to_words(values["rent_amount"])
        else:
            values["rent_amount_words"] = ""

        rendered = template_text
        for key, value in values.items():
            rendered = rendered.replace(f"{{{key}}}", value)
        return rendered

    def generate_docx(self, template_text: str, values: dict[str, str]) -> Path:
        rendered = self.render_template(template_text, values)
        contract_number = values.get("contract_number", "no_number") or "no_number"
        date_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"contract_{contract_number}_{date_stamp}.docx"
        output_path = self.generated_dir / file_name

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx:
            docx.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
            docx.writestr("_rels/.rels", RELS_XML)
            docx.writestr("word/_rels/document.xml.rels", DOC_RELS_XML)
            docx.writestr("word/document.xml", _build_document_xml(rendered))

        return output_path
