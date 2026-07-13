# Tour price calculator

[![Tests](https://github.com/dbasova577-create/Practice/actions/workflows/tests.yml/badge.svg)](https://github.com/dbasova577-create/Practice/actions/workflows/tests.yml)

Самостоятельный Python-модуль расчёта стоимости тура с unit- и интеграционными тестами на pytest. Формула:

```text
round(nights × price_per_night_per_person × (adults + children × 0.5) × (1 − discount))
```

Округление денежных половин выполняется по `ROUND_HALF_UP`. Параметр `board` пока не влияет на итог — это явно закреплено тестом.

## Требования

- Python 3.13;
- зависимости из `requirements-dev.txt` с зафиксированными версиями.

## Локальный запуск

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m pytest
```

Linux/macOS:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

Отдельные наборы:

```bash
python -m pytest --no-cov tests/unit
python -m pytest --no-cov -m integration
```

Обычный запуск `pytest` автоматически:

- проверяет unit- и integration-тесты;
- измеряет line и branch coverage;
- завершает процесс с ошибкой при покрытии ниже 80%;
- создаёт `coverage.xml` и HTML-отчёт в `htmlcov/`.

## Структура

```text
src/tour_price/calculator.py     — формула и валидация
src/tour_price/case_loader.py    — загрузка JSON независимо от CWD
src/tour_price/service.py        — интеграция загрузчика и калькулятора
tests/unit/                      — изолированные unit-тесты
tests/integration/               — проверка полного JSON-пайплайна
DEFECTS.md                       — список найденных и исправленных дефектов
```

## CI

GitHub Actions запускается на `push` и `pull_request`. Порог покрытия является блокирующим. XML- и HTML-отчёты загружаются в artifact `coverage-report`, поэтому зелёный pipeline одновременно подтверждает прохождение тестов и coverage ≥ 80%.

## Репозиторная гигиена

`.idea`, виртуальные окружения, кэши Python и локальные coverage-файлы исключены через `.gitignore`. Если эти файлы уже отслеживаются в старой версии репозитория, перед следующим коммитом их нужно удалить из индекса:

```bash
git rm -r --cached --ignore-unmatch .idea __pycache__ .pytest_cache
git rm --cached --ignore-unmatch .coverage
```
