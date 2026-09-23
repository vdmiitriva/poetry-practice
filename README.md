# Poetry Practice

## Цель проекта

Проект предназначен для работы с банковскими операциями клиента.

В проекте реализованы функции для обработки данных:

* фильтрация операций по статусу;
* сортировка операций по дате;
* фильтрация транзакций по валюте;
* получение описаний транзакций;
* генерация номеров банковских карт.

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

---

### Функция filter_by_currency

Функция `filter_by_currency` возвращает генератор транзакций, отфильтрованных по коду валюты.

Пример использования:

```python
from src.generators import filter_by_currency

transactions = [
    {
        "operationAmount": {
            "currency": {
                "code": "USD"
            }
        }
    },
    {
        "operationAmount": {
            "currency": {
                "code": "RUB"
            }
        }
    },
]

result = list(filter_by_currency(transactions, "USD"))

print(result)
```

Результат:

```python
[
    {
        "operationAmount": {
            "currency": {
                "code": "USD"
            }
        }
    }
]
```

---

### Функция transaction_descriptions

Функция `transaction_descriptions` возвращает генератор с описаниями операций.

Пример использования:

```python
from src.generators import transaction_descriptions

result = transaction_descriptions(transactions)

for description in result:
    print(description)
```

Генератор последовательно возвращает описание каждой транзакции.

---

### Функция card_number_generator

Функция `card_number_generator` генерирует номера карт в заданном диапазоне.

Номер карты возвращается в формате `XXXX XXXX XXXX XXXX`.

Пример использования:

```python
from src.generators import card_number_generator

result = card_number_generator(1, 3)

for card_number in result:
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
```

## Проверка качества кода

Для проверки проекта использовались:

* flake8;
* mypy;
* isort.

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

* flake8 — ошибок не обнаружено;
* mypy — ошибок не обнаружено;
* isort — ошибок форматирования импортов не обнаружено.

## Тестирование

Для запуска всех тестов используется команда:

```bash
poetry run pytest
```

Для проверки покрытия кода:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Для создания HTML-отчёта о покрытии:

```bash
poetry run pytest --cov=src --cov-report=html
```

Результат покрытия:

* общее покрытие — 100%;
* `generators.py` — 100%;
* `masks.py` — 100%;
* `processing.py` — 100%;
* `widget.py` — 100%.

HTML-отчёт сохраняется в папке `htmlcov/`.
