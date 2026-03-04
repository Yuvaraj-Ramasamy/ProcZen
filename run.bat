@echo off
setlocal
cd /d "%~dp0"
call .venv\Scripts ctivate
python proczen.py
if "%~1"=="" pause
endlocal