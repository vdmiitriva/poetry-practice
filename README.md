# Poetry Practice

## Цель проекта

Проект предназначен для работы с банковскими операциями клиента.

В проекте реализованы функции для обработки данных:

* загрузка банковских операций из JSON-, CSV- и XLSX-файлов;
* фильтрация операций по статусу;
* сортировка операций по дате;
* фильтрация транзакций по валюте;
* получение описаний транзакций;
* генерация номеров банковских карт;
* логирование выполнения функций с помощью декоратора `log`;
* логирование работы модулей `masks` и `utils`.

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

Для работы с CSV- и XLSX-файлами используются библиотеки `pandas` и `openpyxl`. Они устанавливаются вместе с остальными зависимостями проекта.

4. Создать файл `.env` в корне проекта и добавить API-ключ:

```text
API_KEY=your_api_key
```

Пример переменной окружения находится в файле `.env.example`.

## Использование

### Загрузка операций из файлов

В модуле `utils` реализованы три функции для загрузки банковских операций:

* `load_operations(file_path)` — загружает операции из JSON-файла;
* `load_operations_from_csv(file_path)` — загружает операции из CSV-файла;
* `load_operations_from_excel(file_path)` — загружает операции из Excel-файла формата XLSX.

Все три функции возвращают список словарей, в котором каждый словарь представляет одну банковскую операцию.

Если указанный файл не найден, функция записывает сообщение в лог и возвращает пустой список. При загрузке JSON также обрабатывается некорректный формат данных и отсутствие списка операций в файле.

#### Загрузка из JSON

```python
from src.utils import load_operations

operations = load_operations("operations.json")
print(operations)
```

#### Загрузка из CSV

```python
from src.utils import load_operations_from_csv

operations = load_operations_from_csv("transactions.csv")
print(operations)
```

Для чтения CSV используется `pandas`. Разделитель столбцов в файле — точка с запятой (`;`).

#### Загрузка из Excel

```python
from src.utils import load_operations_from_excel

operations = load_operations_from_excel("transactions_excel.xlsx")
print(operations)
```

Для чтения XLSX используется `pandas`, а `openpyxl` обеспечивает работу с файлами Excel.

---

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

---

### Декоратор log

Декоратор `log` записывает информацию о выполнении функции.

По умолчанию сообщение выводится в консоль:

```python
from src.decorators import log


@log()
def add(a, b):
    return a + b


add(2, 3)
```

Результат:

```text
add ok
```

Также можно указать имя файла, в который будет записываться лог:

```python
@log("log.txt")
def multiply(a, b):
    return a * b
```

При успешном выполнении функции в файл записывается:

```text
multiply ok
```

Если во время выполнения функции возникает ошибка, декоратор записывает информацию об ошибке и переданных параметрах:

```text
divide error: division by zero. Inputs: (10, 0), {}
```

После записи ошибки исходное исключение передаётся дальше.

---

### Логирование модулей masks и utils

Для модулей `masks` и `utils` используется стандартный модуль Python `logging`.

Для каждого модуля создан отдельный логгер и отдельный файл:

```text
logs/
├── masks.log
└── utils.log
```

Формат записей:

```text
время - имя модуля - уровень - сообщение
```

Например:

```text
2026-10-06 19:55:45,289 - src.masks - INFO - Номер карты успешно замаскирован
```

Успешные операции записываются с уровнем `INFO`, а ошибки — с уровнем `ERROR`.

Логи записываются в кодировке UTF-8. Файлы логов открываются в режиме перезаписи, поэтому при каждом новом запуске соответствующего модуля старые записи заменяются новыми.

Папка `logs` создаётся автоматически при запуске модулей и добавлена в `.gitignore`, поэтому файлы логов не добавляются в Git.

## Проверка качества кода

Для проверки форматирования, стиля кода и порядка импортов используются:

* Black;
* Flake8;
* isort.

Команды для запуска проверок:

```bash
poetry run black .
```

```bash
poetry run flake8 .
```

```bash
poetry run isort --check-only .
```

Black форматирует код, Flake8 проверяет соблюдение правил стиля, а isort проверяет порядок импортов.

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

HTML-отчёт сохраняется в папке `htmlcov/`.

Тесты проекта проверяют существующие функции и новые возможности загрузки операций из CSV- и XLSX-файлов, включая успешное чтение данных и обработку отсутствующих файлов.