# Poetry Practice

## Цель проекта

Проект предназначен для работы с банковскими операциями клиента.

В проекте реализованы функции для обработки данных:

- фильтрация операций по статусу;
- сортировка операций по дате.

## Установка

1. Клонировать репозиторий:

```bash
git clone git@github.com:vdmiitriva/poetry-practice.git
```

2. Перейти в папку проекта:

```bash
cd poetry-practice
```

3. Установить зависимости:

```bash
poetry install
```

## Использование

### Функция filter_by_state

Функция `filter_by_state` фильтрует список операций по значению ключа `state`.

По умолчанию функция выбирает операции со статусом:

```python
"EXECUTED"
```

Пример использования:

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "CANCELED"},
]

result = filter_by_state(operations)

print(result)
```

Результат:

```python
[
    {"id": 1, "state": "EXECUTED"}
]
```

Также можно передать другой статус:

```python
filter_by_state(operations, "CANCELED")
```

Результат:

```python
[
    {"id": 2, "state": "CANCELED"}
]
```

---

### Функция sort_by_date

Функция `sort_by_date` сортирует список операций по дате.

По умолчанию сортировка выполняется по убыванию даты — от новых операций к старым:

```python
from src.processing import sort_by_date

result = sort_by_date(operations)
```

Для сортировки от старых операций к новым необходимо передать параметр:

```python
sort_by_date(operations, reverse=False)
```

Пример:

```python
operations = [
    {"date": "2024-01-15"},
    {"date": "2024-05-20"},
    {"date": "2024-03-11"},
]

result = sort_by_date(operations)
```

Результат:

```python
[
    {"date": "2024-05-20"},
    {"date": "2024-03-11"},
    {"date": "2024-01-15"}
]
```

## Проверка качества кода

Для проверки проекта использовались:

- flake8;
- mypy;
- isort.

Команды для запуска проверок:

```bash
poetry run flake8 .
```

```bash
poetry run mypy .
```

```bash
poetry run isort --check-only .
```

Результаты проверки:

- flake8 — ошибок не обнаружено;
- mypy — ошибок не обнаружено;
- isort — ошибок форматирования импортов не обнаружено.