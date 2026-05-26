@echo off
REM Первичная настройка: venv + зависимости + миграции БД.
REM Запускать из корня проекта или двойным кликом (cd в корень делается ниже).
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo [setup] Создаю виртуальное окружение .venv ...
    py -3 -m venv .venv || python -m venv .venv
    if errorlevel 1 (
        echo [setup] ОШИБКА: не удалось создать venv. Проверь, что Python установлен.
        pause
        exit /b 1
    )
)

echo [setup] Устанавливаю зависимости ...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [setup] ОШИБКА установки зависимостей.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [setup] ВНИМАНИЕ: файла .env нет. Скопируй .env.example в .env и заполни значения.
    pause
    exit /b 1
)

echo [setup] Применяю миграции (alembic upgrade head) ...
call ".venv\Scripts\alembic.exe" upgrade head
if errorlevel 1 (
    echo [setup] ОШИБКА миграций. Проверь доступ к PostgreSQL в .env.
    pause
    exit /b 1
)

echo [setup] Готово. Запускай web через scripts\run-web.bat
pause
