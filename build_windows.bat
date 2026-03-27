@echo off
setlocal
chcp 65001 >nul

cd /d "%~dp0"

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo [2/4] Cleaning previous build folders...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [3/4] Building portable onedir EXE...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onedir ^
  --name trust_communal_contract_generator ^
  --add-data "templates;templates" ^
  main.py

echo [4/4] Creating runtime folders near EXE...
if not exist "dist\trust_communal_contract_generator\data" mkdir "dist\trust_communal_contract_generator\data"
if not exist "dist\trust_communal_contract_generator\generated" mkdir "dist\trust_communal_contract_generator\generated"
if not exist "dist\trust_communal_contract_generator\settings" mkdir "dist\trust_communal_contract_generator\settings"
if not exist "dist\trust_communal_contract_generator\templates" mkdir "dist\trust_communal_contract_generator\templates"

echo.
echo Done. Portable build folder:
echo dist\trust_communal_contract_generator\
echo Copy this whole folder to another computer.

endlocal
