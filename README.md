# TRUST COMMUNAL Contract Generator

Простое настольное приложение для Windows (Tkinter) для работы с шаблонами договоров и генерации `.docx`.

## Запуск в режиме разработки

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python main.py
```

## Функции

- Сохранение реквизитов арендодателя в `settings/landlord_details.json`.
- Управление шаблонами договоров в папке `templates/`.
- Генерация договоров в формате `.docx` в папке `generated/`.
- Автоматический расчёт суммы прописью (`{rent_amount_words}`).

## Переменные шаблона

- `{contract_number}`
- `{contract_date}`
- `{tenant_name}`
- `{tenant_director}`
- `{tenant_basis}`
- `{tenant_address}`
- `{object_address}`
- `{area_sq_m}`
- `{rent_amount}`
- `{rent_amount_words}`
- `{term_text}`
- `{landlord_name}`
- `{landlord_director}`
- `{landlord_basis}`
- `{landlord_address}`
- `{landlord_details}`

Подробная сборка `.exe`: см. `BUILD_WINDOWS_EXE.md`.
