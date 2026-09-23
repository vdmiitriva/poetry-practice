def filter_by_currency(data: list[dict], cur: str):
    for d in data:
        if d["operationAmount"]["currency"]["code"] == cur:
            yield d