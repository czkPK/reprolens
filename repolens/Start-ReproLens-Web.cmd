@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONPATH=%~dp0src"
python -m repolens.web --open
if errorlevel 1 pause
