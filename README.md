# softForMarket

Сервис автоматизации заказов для GGSEL и Digiseller/PLATI: клиент покупает товар
(Telegram-бусты) на площадке → редирект на наш домен → заказ размещается у поставщика
**TeaTeaGram** → уведомление в Telegram-группу → клиент отслеживает статус на `/status`.

## Стек

FastAPI (async) · SQLAlchemy 2.0 + asyncpg (PostgreSQL) · Alembic · httpx · loguru · Jinja2.

## Структура

```
app/
  api/v1/routes/      # ggsel, digiseller, status, misc (health, /)
  clients/            # внешние API: telegram, suppliers/teateagram, platforms/ggsel|digiseller (BaseApi)
  core/config/        # settings (.env) + services.yaml (каталог товаров)
  db/                 # models, repository, session (engine)
  services/           # links (парсеры), orders (оркестратор), background (asyncio-задачи)
  templates/          # status.html
  main.py             # FastAPI app + lifespan
  worker.py           # фоновый процесс (поллер чатов GGSEL)
alembic/              # миграции
config/               # config.yaml (логи), services.yaml (товары→услуги)
```

## Конфигурация

Все настройки — в `.env` (см. `.env.example`). Секреты: токены Telegram/GGSEL/Digiseller/TeaTeaGram,
SOCKS5-прокси для Telegram, доступ к PostgreSQL. Каталог товаров — в `config/services.yaml`.

## Запуск (Docker)

```bash
cp .env.example .env        # заполнить значения
alembic upgrade head        # миграции выполняются вручную (схема marketplace)
docker compose up -d --build
```

Сервисы:
- **app** — web (uvicorn, порт 80→8000). Масштаб через `WORKERS` (по умолчанию 2).
- **worker** — фоновый поллер чатов GGSEL. Ровно один экземпляр (не масштабировать).

Отложенные проверки статуса заказа создаются per-request в web и не дублируются.

## Локальный запуск

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload          # web
python -m app.worker                    # фоновый процесс (отдельно)
```

## Эндпоинты (под `/api/v1`)

| Метод | Путь | Назначение |
|---|---|---|
| GET | `/api/v1/health` | проверка живости |
| GET | `/api/v1/ggsel?uniquecode=` | callback GGSEL |
| GET | `/api/v1/digiseller-callback?uniquecode=` | callback PLATI |
| GET | `/api/v1/status?code=` | страница статуса заказа |
| GET | `/api/v1/openapi` | Swagger UI |

> Callback-URL в кабинетах GGSEL/Plati должны указывать на `https://<домен>/api/v1/...`.

## Качество кода

```bash
make all        # ruff (fix+format) + mypy
```

## Миграции

```bash
alembic revision --autogenerate -m "описание"   # создать
alembic upgrade head                              # применить
alembic downgrade -1                              # откатить
```
