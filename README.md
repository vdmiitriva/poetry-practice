# Poetry Practice

## Цель проекта

Проект предназначен для обработки банковских операций клиента. Он позволяет загружать транзакции из разных форматов файлов, фильтровать и сортировать данные, искать операции по описанию и подсчитывать количество операций по категориям.

Основные возможности проекта:

- загрузка банковских операций из JSON-, CSV- и XLSX-файлов;
- фильтрация операций по статусу;
- сортировка операций по дате;
- фильтрация транзакций по валюте;
- поиск операций по описанию с использованием регулярных выражений;
- подсчёт количества операций по заданным категориям;
- получение описаний транзакций с помощью генератора;
- генерация номеров банковских карт;
- маскировка номеров банковских карт и счетов;
- форматирование дат;
- получение курсов валют и конвертация сумм в рубли;
- логирование выполнения функций с помощью декоратора `log`;
- логирование работы модулей `masks` и `utils`;
- интерактивная обработка банковских операций через `main.py`.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone git@github.com:vdmiitriva/poetry-practice.git
   ```

2. Перейдите в папку проекта:

   ```bash
   cd poetry-practice
   ```

3. Установите зависимости:

   ```bash
   poetry install
   ```

   Для работы с CSV- и XLSX-файлами используются библиотеки `pandas` и `openpyxl`. Они устанавливаются вместе с остальными зависимостями проекта.

4. Для работы модуля конвертации валют создайте файл `.env` в корне проекта и добавьте API-ключ:

   ```text
   API_KEY=your_api_key
   ```

   Пример переменной окружения находится в файле `.env.example`. Получите собственный API-ключ у поставщика используемого API. Не публикуйте настоящий ключ в репозитории.

## Использование

### Запуск программы

Для запуска интерактивной программы выполните команду из корня проекта:

```bash
poetry run python main.py
```

Программа предлагает выбрать файл с банковскими операциями в формате JSON, CSV или XLSX. После загрузки данных пользователь может:

1. Выбрать статус операций для фильтрации: `EXECUTED`, `CANCELED` или `PENDING`.
2. Выбрать, нужно ли сортировать операции по дате.
3. Указать направление сортировки: по возрастанию или по убыванию.
4. Оставить только транзакции в рублях.
5. Найти операции по определённому слову или выражению в описании.
6. Просмотреть итоговый список операций.

Если подходящие транзакции отсутствуют, программа выводит соответствующее сообщение.

### Загрузка операций из файлов

В модуле `utils` реализованы три функции для загрузки банковских операций:

- `load_operations(file_path)` — загружает операции из JSON-файла;
- `load_operations_from_csv(file_path)` — загружает операции из CSV-файла;
- `load_operations_from_excel(file_path)` — загружает операции из Excel-файла формата XLSX.

Функции возвращают список словарей, в котором каждый словарь представляет одну банковскую операцию.

Если указанный файл не найден, функция записывает сообщение в лог и возвращает пустой список. При загрузке JSON также обрабатываются некорректный формат данных и отсутствие списка операций в файле.

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

### Функция `filter_by_state`

Функция `filter_by_state` фильтрует список операций по значению ключа `state`.

По умолчанию выбираются операции со статусом `EXECUTED`.

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
[{"id": 1, "state": "EXECUTED"}]
```

Чтобы выбрать операции с другим статусом, передайте его вторым аргументом:

```python
result = filter_by_state(operations, "CANCELED")
```

Результат:

```python
[{"id": 2, "state": "CANCELED"}]
```

### Функция `sort_by_date`

Функция `sort_by_date` сортирует список операций по дате.

По умолчанию сортировка выполняется по убыванию даты — от новых операций к старым.

```python
from src.processing import sort_by_date

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
    {"date": "2024-01-15"},
]
```

Для сортировки от старых операций к новым используйте параметр `reverse=False`:

```python
result = sort_by_date(operations, reverse=False)
```

### Функция `filter_by_currency`

Функция `filter_by_currency` возвращает генератор транзакций, отфильтрованных по коду валюты.

```python
from src.generators import filter_by_currency

transactions = [
    {"operationAmount": {"currency": {"code": "USD"}}},
    {"operationAmount": {"currency": {"code": "RUB"}}},
]

result = list(filter_by_currency(transactions, "USD"))
print(result)
```

Результат:

```python
[{"operationAmount": {"currency": {"code": "USD"}}}]
```

### Функция `transaction_descriptions`

Функция `transaction_descriptions` возвращает генератор, последовательно выдающий описания операций.

```python
from src.generators import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": "Открытие вклада"},
]

for description in transaction_descriptions(transactions):
    print(description)
```

Результат:

```text
Перевод организации
Открытие вклада
```

### Функция `card_number_generator`

Функция `card_number_generator` генерирует номера банковских карт в заданном диапазоне.

Номер возвращается в формате `XXXX XXXX XXXX XXXX`.

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 3):
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
```

### Функция `process_bank_search`

Функция `process_bank_search` ищет операции, описание которых соответствует поисковому запросу. Поиск выполняется без учёта регистра с помощью регулярных выражений.

```python
from src.processing import process_bank_search

operations = [
    {"description": "Перевод организации"},
    {"description": "Открытие вклада"},
    {"description": "Перевод между счетами"},
]

result = process_bank_search(operations, "перевод")
print(result)
```

Результат содержит операции с описаниями «Перевод организации» и «Перевод между счетами».

### Функция `process_bank_operations`

Функция `process_bank_operations` подсчитывает количество операций, описание которых содержит каждую из заданных категорий.

```python
from src.processing import process_bank_operations

operations = [
    {"description": "Перевод организации"},
    {"description": "Открытие вклада"},
    {"description": "Перевод между счетами"},
]

categories = ["перевод", "вклад", "покупка"]

result = process_bank_operations(operations, categories)
print(result)
```

Результат:

```python
{
    "перевод": 2,
    "вклад": 1,
    "покупка": 0,
}
```

Подсчёт выполняется без учёта регистра. В результате сохраняются все переданные категории, в том числе категории, для которых не найдено ни одной операции.

### Функция `mask_account_card`

Функция `mask_account_card` маскирует номера банковских карт и счетов, сохраняя название карты или тип счёта.

Пример:

```python
from src.widget import mask_account_card

print(mask_account_card("Visa Classic 1234567812341234"))
print(mask_account_card("Счет 1234567890"))
```

Пример результата (сверьте формат с фактической реализацией функции):

```text
Visa Classic 1234 56** **** 1234
Счет **7890
```

### Функция `get_date`

Функция `get_date` преобразует дату в формат `ДД.ММ.ГГГГ`.

```python
from src.widget import get_date

print(get_date("2024-05-20T12:30:00"))
```

Результат:

```text
20.05.2024
```

### Декоратор `log`

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

При успешном выполнении функции записывается сообщение об успешном завершении. Если возникает ошибка, декоратор записывает информацию об ошибке и переданных аргументах, после чего повторно вызывает исходное исключение.

Пример сообщения об ошибке:

```text
divide error: division by zero. Inputs: (10, 0), {}
```

### Логирование модулей `masks` и `utils`

Для модулей `masks` и `utils` используется стандартный модуль Python `logging`.

Для каждого модуля предусмотрен отдельный лог-файл:

```text
logs/
├── masks.log
└── utils.log
```

Формат записей:

```text
время - имя модуля - уровень - сообщение
```

Пример:

```text
2026-10-06 19:55:45,289 - src.masks - INFO - Номер карты успешно замаскирован
```

Успешные операции записываются с уровнем `INFO`, а ошибки — с уровнем `ERROR`.

Логи записываются в кодировке UTF-8. Файлы открываются в режиме перезаписи, поэтому старые записи заменяются новыми при повторном запуске соответствующего модуля. Папка `logs` создаётся автоматически, а файлы логов добавлены в `.gitignore`.

### Модуль `external_api`

Модуль `external_api` предназначен для получения курсов валют через внешний API и конвертации сумм банковских операций в рубли.

Для работы модуля необходимо указать API-ключ в файле `.env`:

```text
API_KEY=your_api_key
```

#### Функция `get_exchange_rate`

Функция `get_exchange_rate` получает курс указанной валюты к рублю через внешний API.

```python
from src.external_api import get_exchange_rate

rate = get_exchange_rate("USD")
print(rate)
```

Функция возвращает курс валюты к рублю в виде числа с плавающей точкой. Для выполнения запроса требуется доступ к API и действительный ключ.

#### Функция `convert_amount`

Функция `convert_amount` конвертирует сумму банковской операции в рубли. Если валюта операции уже указана как `RUB`, сумма возвращается без конвертации. Для остальных валют используется курс, полученный через `get_exchange_rate`.

```python
from src.external_api import convert_amount

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"},
    },
}

amount_in_rubles = convert_amount(transaction)
print(amount_in_rubles)
```

Результат зависит от актуального курса валюты.

## Проверка качества кода

Для форматирования и проверки стиля кода используются Black, Flake8 и isort.

Форматирование кода:

```bash
poetry run black .
```

Проверка стиля:

```bash
poetry run flake8 .
```

Проверка порядка импортов:

```bash
poetry run isort --check-only .
```

Black автоматически форматирует код, Flake8 проверяет соблюдение правил стиля, а isort проверяет порядок импортов.

## Тестирование

Для запуска всех тестов выполните:

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

Тесты проверяют работу функций проекта, включая фильтрацию и сортировку операций, поиск по описанию, подсчёт операций по категориям, маскировку данных, генераторы, логирование и загрузку данных из JSON-, CSV- и XLSX-файлов.

## Используемые технологии

- Python
- Poetry
- pandas
- openpyxl
- requests
- python-dotenv
- pytest
- pytest-cov
- Black
- Flake8
- isort
- logging
