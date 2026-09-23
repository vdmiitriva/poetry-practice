from collections.abc import Iterator


def filter_by_currency(data: list[dict], cur: str) -> Iterator[dict]:
    """Возвращает генератор транзакций с указанной валютой."""
    for d in data:
        if d["operationAmount"]["currency"]["code"] == cur:
            yield d


def transaction_descriptions(data: list[dict]) -> Iterator[str]:
    """Возвращает генератор описания каждой операции по очереди."""
    for d in data:
        yield d["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Возвращает генератор описаний каждой операции по очереди."""
    for number in range(start, end + 1):
        num = str(number).zfill(16)
        card = " ".join(num[i : i + 4] for i in range(0, 16, 4))
        yield card
