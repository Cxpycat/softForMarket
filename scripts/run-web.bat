@echo off
REM Запуск web (uvicorn). Хост и порт берутся из .env (SERVER_HOST / SERVER_PORT).
setlocal enabledelayedexpansion
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [web] Нет .venv. Сначала запусти scripts\setup.bat
    pause
    exit /b 1
)

REM --- читаем SERVER_HOST и SERVER_PORT из .env (строки вида KEY=VALUE) ---
set "HOST="
set "PORT="
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if /i "%%A"=="SERVER_HOST" set "HOST=%%B"
    if /i "%%A"=="SERVER_PORT" set "PORT=%%B"
)
if not defined HOST set "HOST=127.0.0.1"
if not defined PORT set "PORT=8000"
REM срезаем случайные пробелы по краям значений
set "HOST=%HOST: =%"
set "PORT=%PORT: =%"

echo [web] Запуск uvicorn на %HOST%:%PORT% ...
call ".venv\Scripts\python.exe" -m uvicorn app.main:app --host %HOST% --port %PORT%

REM если uvicorn упал — не закрывать окно мгновенно
pause
