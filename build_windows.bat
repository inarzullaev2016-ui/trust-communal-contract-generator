@echo off
setlocal

cd /d "%~dp0"

echo [1/3] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo [2/3] Building portable onedir EXE...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --name trust_communal_contract_generator ^
  --add-data "templates;templates" ^
  --add-data "settings;settings" ^
  --add-data "data;data" ^
  --add-data "generated;generated" ^
  main.py

echo [3/3] Done.
echo Portable build folder: dist\trust_communal_contract_generator
pause
