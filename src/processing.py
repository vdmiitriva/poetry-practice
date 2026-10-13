import re
from collections import Counter
from datetime import datetime


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список операций по статусу."""
    result = []

    for operation in data:
        if operation.get("state") == state:
            result.append(operation)

    return result


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список операций по датам."""

    def parse_date(item: dict) -> datetime:
        date = item["date"].split("T")[0]

        for date_format in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(date, date_format)
            except ValueError:
                continue

        raise ValueError(f"Некорректный формат даты: {date}")

    return sorted(data, key=parse_date, reverse=reverse)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Назодит операции, описание которых соответствует поисковому запросу."""
    result = []

    for operation in data:
        description = str(operation.get("description", ""))
        if re.search(search, description, re.IGNORECASE):
            result.append(operation)

    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций по заданным категориям."""
    descriptions = [str(operation.get("description", "")).lower() for operation in data]

    counts = Counter()

    for category in categories:
        category_name = str(category)
        counts[category_name] = sum(category_name.lower() in description for description in descriptions)

    return dict(counts)
