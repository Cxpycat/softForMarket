@echo off
REM Start web (uvicorn). Host and port are read from .env (SERVER_HOST / SERVER_PORT).
setlocal enabledelayedexpansion
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [web] No .venv found. Run scripts\setup.bat first.
    pause
    exit /b 1
)

REM --- read SERVER_HOST and SERVER_PORT from .env (lines like KEY=VALUE) ---
set "HOST="
set "PORT="
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if /i "%%A"=="SERVER_HOST" set "HOST=%%B"
    if /i "%%A"=="SERVER_PORT" set "PORT=%%B"
)
if not defined HOST set "HOST=127.0.0.1"
if not defined PORT set "PORT=8000"
REM trim stray spaces around the values
set "HOST=%HOST: =%"
set "PORT=%PORT: =%"

echo [web] Starting uvicorn on %HOST%:%PORT% ...
call ".venv\Scripts\python.exe" -m uvicorn app.main:app --host %HOST% --port %PORT%

REM if uvicorn crashed, do not close the window immediately
pause
