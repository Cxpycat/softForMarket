@echo off
REM Start the background worker (GGSEL chat poller). Exactly one instance.
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [worker] No .venv found. Run scripts\setup.bat first.
    pause
    exit /b 1
)

echo [worker] Starting app.worker ...
call ".venv\Scripts\python.exe" -m app.worker

pause
