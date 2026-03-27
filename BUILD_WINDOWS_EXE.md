# Сборка portable `.exe` для Windows 10/11

## 1) Подготовка

1. Установите Python 3.11+ на Windows.
2. Откройте PowerShell в папке проекта.

## 2) Установка зависимостей

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
```

## 3) Сборка

```powershell
pyinstaller --noconfirm --onefile --windowed --name trust_contract_generator main.py
```

## 4) Формирование portable-папки

После сборки создайте рядом с `.exe` папки:

- `templates/`
- `data/`
- `generated/`
- `settings/`

Скопируйте в `templates/` ваши шаблоны (или оставьте автосоздание пустых папок при первом запуске).

Итоговая portable-папка должна содержать:

- `trust_contract_generator.exe`
- `templates/`
- `data/`
- `generated/`
- `settings/`

Эту папку можно переносить на другой компьютер простым копированием.

## Важно

- Приложение использует только относительные пути от местоположения `.exe`.
- Все пользовательские данные и сгенерированные договоры сохраняются рядом с программой.
