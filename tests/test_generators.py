from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
    expected_count: int,
) -> None:
    result = list(filter_by_currency(transactions, currency))

    assert len(result) == expected_count
    assert all(transaction["operationAmount"]["currency"]["code"] == currency for transaction in result)


def test_filter_by_currency_empty_list() -> None:
    result = list(filter_by_currency([], "USD"))

    assert result == []


def test_transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> None:
    result = list(transaction_descriptions(transactions))

    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    result = list(transaction_descriptions([]))

    assert result == []


@pytest.mark.parametrize(
    "position, expected",
    [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (2, "Перевод со счета на счет"),
    ],
)
def test_transaction_descriptions_generator(
    transactions: list[dict[str, Any]],
    position: int,
    expected: str,
) -> None:
    result = transaction_descriptions(transactions)

    for _ in range(position + 1):
        description = next(result)

    assert description == expected


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            123,
            123,
            ["0000 0000 0000 0123"],
        ),
        (
            9999999999999999,
            9999999999999999,
            ["9999 9999 9999 9999"],
        ),
    ],
)
def test_card_number_generator(
    start: int,
    end: int,
    expected: list[str],
) -> None:
    result = list(card_number_generator(start, end))

    assert result == expected


@pytest.mark.parametrize(
    "start, end",
    [
        (1, 5),
        (100, 105),
        (9999, 10004),
    ],
)
def test_card_number_generator_format(start: int, end: int) -> None:
    result = list(card_number_generator(start, end))

    assert all(len(card.replace(" ", "")) == 16 for card in result)
    assert all(card.count(" ") == 3 for card in result)
