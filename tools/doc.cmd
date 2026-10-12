@echo off
rem Инструмент правил документации (Windows): tools\doc.cmd route|next|diagram|pre|post|check|staged|generated|rnd ...
set "ROOT=%~dp0.."
set "PY=python"
if exist "%ROOT%\html-view\.venv\Scripts\python.exe" set "PY=%ROOT%\html-view\.venv\Scripts\python.exe"
set PYTHONIOENCODING=utf-8
"%PY%" "%ROOT%\html-view\doctool.py" %*
