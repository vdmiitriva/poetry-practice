def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список операций по статусу."""
    result = []

    for i in data:
        if i.get("state") == state:
            result.append(i)

    return result


