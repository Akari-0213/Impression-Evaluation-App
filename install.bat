@echo off

set VENV=%~dp0venv
cd /d "%~dp0"

py -3.11 -m venv "%VENV%"
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
"%VENV%\Scripts\python.exe" -m pip install -r "%~dp0\requirements.txt"
