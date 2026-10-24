@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_repolens.ps1" -Path "%~dp0examples\demo-llm-app"
if errorlevel 1 pause
