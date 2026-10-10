@echo off
rem Local preview of HTML docs: http://127.0.0.1:8000
rem First run creates html-view\.venv and installs MkDocs.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv ...
  python -m venv .venv || goto :error
)
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt || goto :error
start "" "http://127.0.0.1:8000"
".venv\Scripts\python.exe" build.py serve
goto :eof

:error
echo Error: Python 3.10+ is required in PATH.
pause
