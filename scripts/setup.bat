@echo off
REM Initial setup: venv + dependencies + DB migrations.
REM Run from the project root or by double-clicking (cd to root is done below).
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment .venv ...
    py -3 -m venv .venv || python -m venv .venv
    if errorlevel 1 (
        echo [setup] ERROR: failed to create venv. Make sure Python is installed.
        pause
        exit /b 1
    )
)

echo [setup] Installing dependencies ...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [setup] ERROR installing dependencies.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [setup] WARNING: .env file is missing. Copy .env.example to .env and fill in the values.
    pause
    exit /b 1
)

echo [setup] Applying migrations (alembic upgrade head) ...
call ".venv\Scripts\alembic.exe" upgrade head
if errorlevel 1 (
    echo [setup] ERROR running migrations. Check PostgreSQL access in .env.
    pause
    exit /b 1
)

echo [setup] Done. Start web with scripts\run-web.bat
pause
