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

## 3) Сборка portable (рекомендуется)

```powershell
.\build_windows.bat
```

Скрипт автоматически:

- ставит зависимости;
- очищает `build/` и `dist/`;
- собирает `onedir`-версию через PyInstaller;
- создаёт рядом с `.exe` рабочие папки `templates/`, `data/`, `generated/`, `settings/`.

## 4) Формирование portable-папки вручную (альтернатива)

Если хотите собрать без `.bat`, используйте:

```powershell
pyinstaller --noconfirm --clean --windowed --onedir --name trust_communal_contract_generator --add-data "templates;templates" main.py
```

После сборки создайте рядом с `.exe` папки:

- `templates/`
- `data/`
- `generated/`
- `settings/`

Скопируйте в `templates/` ваши шаблоны (или оставьте автосоздание пустых папок при первом запуске).

Итоговая portable-папка должна содержать:

- `trust_communal_contract_generator.exe` (внутри `dist/trust_communal_contract_generator/`)
- `templates/`
- `data/`
- `generated/`
- `settings/`

Эту папку можно переносить на другой компьютер простым копированием.

## Важно

- Приложение использует только относительные пути от местоположения `.exe`.
- Все пользовательские данные и сгенерированные договоры сохраняются рядом с программой.
