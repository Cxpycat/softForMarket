@echo off
REM Запуск фонового worker (поллер чатов GGSEL). Ровно один экземпляр.
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [worker] Нет .venv. Сначала запусти scripts\setup.bat
    pause
    exit /b 1
)

echo [worker] Запуск app.worker ...
call ".venv\Scripts\python.exe" -m app.worker

pause
