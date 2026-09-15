# Poetry Practice

## Цель проекта

Проект предназначен для работы с банковскими операциями. В проекте реализованы функции для фильтрации операций по статусу и сортировки операций по дате.

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

### filter_by_state

Функция `filter_by_state` фильтрует список операций по статусу.

По умолчанию используются операции со статусом `EXECUTED`:

```python
filter_by_state(operations)
```

Чтобы выбрать другой статус:

```python
filter_by_state(operations, "CANCELED")
```

### sort_by_date

Функция `sort_by_date` сортирует операции по дате.

По умолчанию операции сортируются от новых к старым:

```python
sort_by_date(operations)
```

Для сортировки от старых к новым:

```python
sort_by_date(operations, reverse=False)
```

## Пример

```python
operations = [
    {"date": "2024-03-11", "state": "EXECUTED"},
    {"date": "2024-05-20", "state": "CANCELED"},
    {"date": "2024-01-15", "state": "EXECUTED"},
]

executed_operations = filter_by_state(operations)

sorted_operations = sort_by_date(operations)
```
