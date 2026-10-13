from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_operations, load_operations_from_csv, load_operations_from_excel
from src.widget import get_date, mask_account_card


def ask_yes_no(question: str) -> bool:
    """Запрашивает ответ да или нет."""
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, ответьте «да» или «нет».")


def choose_file() -> list[dict]:
    """Предлагает формат файла и загружает операции."""
    loaders = {
        "1": ("data/operations.json", load_operations),
        "2": ("transactions.csv", load_operations_from_csv),
        "3": ("transactions_excel.xlsx", load_operations_from_excel),
    }

    while True:
        print("\nВыберите файл с операциями:")
        print("1. JSON")
        print("2. CSV")
        print("3. XLSX")

        choice = input("Ваш выбор: ").strip()

        if choice not in loaders:
            print("Нужно выбрать 1, 2 или 3.")
            continue

        file_path, loader = loaders[choice]
        operations = loader(file_path)

        if operations:
            print(f"Загружено операций: {len(operations)}")
        else:
            print("Не удалось загрузить операции или файл пуст.")

        return operations


def get_currency(operation: dict) -> str:
    """Возвращает код валюты операции для разных форматов."""
    amount_data = operation.get("operationAmount") or {}
    currency_data = amount_data.get("currency") or {}

    return str(currency_data.get("code") or operation.get("currency_code") or "")


def choose_status(operations: list[dict]) -> list[dict]:
    """Запрашивает статус и фильтрует операции."""
    available_statuses = ("EXECUTED", "CANCELED", "PENDING")

    while True:
        print("Введите статус для фильтрации.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")

        status = input("Ваш выбор: ").strip().upper()

        if status in available_statuses:
            print(f'Операции отфильтрованы по статусу "{status}".')
            return filter_by_state(operations, status)

        print(f'Статус операции "{status}" недоступен.')


def sort_operations(operations: list[dict]) -> list[dict]:
    """Предлагает отсортировать операции по дате."""
    if not ask_yes_no("Отсортировать операции по дате? Да/Нет: "):
        return operations

    while True:
        order = input("Сортировать по возрастанию или по убыванию? ").strip().lower()

        if order in ("по возрастанию", "возрастанию"):
            return sort_by_date(operations, reverse=False)

        if order in ("по убыванию", "убыванию"):
            return sort_by_date(operations, reverse=True)

        print("Введите «по возрастанию» или «по убыванию».")


def filter_operations(operations: list[dict]) -> list[dict]:
    """Фильтрует операции по валюте и описанию."""
    if ask_yes_no("Выводить только рублёвые транзакции? Да/Нет: "):
        operations = [operation for operation in operations if get_currency(operation) == "RUB"]

    if ask_yes_no("Отфильтровать список транзакций по слову в описании? Да/Нет: "):
        search = input("Введите строку поиска: ").strip()

        if search:
            operations = process_bank_search(operations, search)

    return operations


def print_operation(operation: dict) -> None:
    """Выводит информацию о банковской операции."""
    date = get_date(str(operation["date"]))
    description = operation.get("description", "Без описания")

    print(f"{date} {description}")

    amount_data = operation.get("operationAmount") or {}
    currency_data = amount_data.get("currency") or {}

    amount = amount_data.get("amount", operation.get("amount", 0))
    currency = (
        currency_data.get("name")
        or operation.get("currency_name")
        or currency_data.get("code")
        or operation.get("currency_code")
        or ""
    )

    sender = operation.get("from")
    recipient = operation.get("to")

    if sender and recipient:
        print(f"{mask_account_card(str(sender))} -> " f"{mask_account_card(str(recipient))}")
    elif sender:
        print(mask_account_card(str(sender)))
    elif recipient:
        print(mask_account_card(str(recipient)))

    print(f"Сумма: {amount} {currency}")
    print()


def main() -> None:
    """Запускает программу обработки банковских транзакций."""
    print("Привет! Добро пожаловать в программу работы " "с банковскими транзакциями.")

    operations = choose_file()

    if not operations:
        print("Нет данных для обработки.")
        return

    filtered_operations = choose_status(operations)
    filtered_operations = sort_operations(filtered_operations)
    filtered_operations = filter_operations(filtered_operations)

    if not filtered_operations:
        print("Не найдено ни одной транзакции, подходящей " "под ваши условия фильтрации.")
        return

    print("Распечатываю итоговый список транзакций...")
    print("Всего банковских операций в выборке: " f"{len(filtered_operations)}")

    for operation in filtered_operations:
        print_operation(operation)


if __name__ == "__main__":
    main()
