.PHONY: help all format lint fix typecheck test check

# Команда по умолчанию — короткая и полная: формат + автофикс + lint + типы
.DEFAULT_GOAL := all

help:  ## Показать список целей
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

# Основная цель: отформатировать, починить что можно, прогнать lint и типы
all: fix typecheck  ## Форматирование + автофиксы + ruff check + mypy

format:  ## Только форматирование
	ruff format app tests

lint:  ## Только проверки без правок
	ruff check app tests

fix:  ## Автофиксы + форматирование
	ruff check --fix app tests
	ruff format app tests

typecheck:  ## Проверка типов (mypy)
	mypy app

test:  ## Запуск тестов
	pytest -q

check: all test  ## Полная проверка: lint + типы + тесты
