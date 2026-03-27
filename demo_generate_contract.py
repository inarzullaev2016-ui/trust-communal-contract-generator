from __future__ import annotations

from pathlib import Path

from app.contract_service import ContractService
from app.path_utils import get_app_root, ensure_project_dirs
from app.storage import load_json


def main() -> None:
    root = get_app_root()
    dirs = ensure_project_dirs(root)

    template_path = dirs["templates"] / "test_lease_template.txt"
    template_text = template_path.read_text(encoding="utf-8")

    landlord = load_json(
        dirs["settings"] / "landlord.json",
        {
            "landlord_name": "ТОО TRUST COMMUNAL",
            "landlord_director": "Иванов И.И.",
            "landlord_basis": "Устава",
            "landlord_address": "г. Астана, ул. Пример, 1",
            "landlord_details": "БИН 123456789012, ИИК KZ000000000000000000",
        },
    )

    values = {
        "contract_number": "TEST-001",
        "contract_date": "27.03.2026",
        "tenant_name": "ТОО Тест Арендатор",
        "tenant_director": "Петров П.П.",
        "tenant_basis": "Устава",
        "tenant_address": "г. Астана, ул. Тестовая, 2",
        "object_address": "г. Астана, ул. Объект, 7",
        "area_sq_m": "120",
        "rent_amount": "350000",
        "term_text": "11 месяцев",
        **landlord,
    }

    service = ContractService(dirs["generated"])
    output = service.generate_docx(template_text, values)
    print(f"Created: {output}")


if __name__ == "__main__":
    main()
