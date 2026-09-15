def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список операций по статусу."""
    result = []

    for i in data:
        if i.get("state") == state:
            result.append(i)

    return result


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список операций по дате."""
    return sorted(data, key=lambda item: item["date"], reverse=reverse)
