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
        date = item["date"]

        for date_format in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(date, date_format)
            except ValueError:
                continue

        raise ValueError(f"Некорректный формат даты: {date}")

    return sorted(data, key=parse_date, reverse=reverse)
