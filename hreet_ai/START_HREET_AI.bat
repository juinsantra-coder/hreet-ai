@echo off
cd /d "%~dp0"
echo Starting HREET AI Orange Nexus...
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo HREET AI will open at http://127.0.0.1:8000
start "HREET AI" http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
