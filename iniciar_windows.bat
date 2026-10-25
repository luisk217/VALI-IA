@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Primero sigue la instalacion de README.md para crear el entorno .venv.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run app.py
pause
