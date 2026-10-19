import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


@pytest.fixture
def operations() -> list[dict]:
    return [
        {
            "state": "EXECUTED",
            "date": "2024-03-15",
        },
        {
            "state": "CANCELED",
            "date": "2024-03-10",
        },
        {
            "state": "EXECUTED",
            "date": "2024-03-20",
        },
        {
            "state": "PENDING",
            "date": "2024-03-05",
        },
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 1),
        ("UNKNOWN", 0),
    ],
)
def test_filter_by_state(
    operations: list[dict],
    state: str,
    expected_count: int,
) -> None:
    result = filter_by_state(operations, state)
    assert len(result) == expected_count


def test_filter_by_state_without_state() -> None:
    data = [
        {"date": "2024-03-15"},
        {"state": "EXECUTED", "date": "2024-03-20"},
    ]

    result = filter_by_state(data)

    assert result == [
        {"state": "EXECUTED", "date": "2024-03-20"},
    ]


@pytest.mark.parametrize(
    "reverse",
    [True, False],
)
def test_sort_by_date(
    operations: list[dict],
    reverse: bool,
) -> None:
    result = sort_by_date(operations, reverse=reverse)

    dates = [operation["date"] for operation in result]

    if reverse:
        assert dates == [
            "2024-03-20",
            "2024-03-15",
            "2024-03-10",
            "2024-03-05",
        ]
    else:
        assert dates == [
            "2024-03-05",
            "2024-03-10",
            "2024-03-15",
            "2024-03-20",
        ]


def test_sort_by_date_same_dates() -> None:
    data = [
        {"date": "2024-03-15", "id": 1},
        {"date": "2024-03-15", "id": 2},
        {"date": "2024-03-10", "id": 3},
    ]

    result = sort_by_date(data)

    assert result == [
        {"date": "2024-03-15", "id": 1},
        {"date": "2024-03-15", "id": 2},
        {"date": "2024-03-10", "id": 3},
    ]


def test_sort_by_date_different_formats() -> None:
    data = [
        {"date": "15.03.2024"},
        {"date": "01.12.2023"},
        {"date": "20.01.2024"},
    ]

    result = sort_by_date(data)

    assert result == [
        {"date": "15.03.2024"},
        {"date": "20.01.2024"},
        {"date": "01.12.2023"},
    ]


def test_sort_by_date_invalid_date() -> None:
    data = [
        {"date": "2024-03-15"},
        {"date": "не дата"},
    ]

    with pytest.raises(ValueError):
        sort_by_date(data)


def test_process_bank_search() -> None:
    data = [
        {"description": "Перевод организации", "id": 1},
        {"description": "Оплата товаров", "id": 2},
        {"description": "Перевод со счета", "id": 3},
    ]

    result = process_bank_search(data, "перевод")

    assert [operation["id"] for operation in result] == [1, 3]


def test_process_bank_search_no_matches() -> None:
    data = [{"description": "Оплата товаров"}]

    assert process_bank_search(data, "перевод") == []


def test_process_bank_search_missing_description() -> None:
    data = [{"id": 1}, {"description": "Перевод организации"}]

    assert process_bank_search(data, "перевод") == [{"description": "Перевод организации"}]


def test_process_bank_operations() -> None:
    data = [
        {"description": "Перевод организации"},
        {"description": "Оплата товаров"},
        {"description": "Перевод со счета"},
        {"description": "Оплата услуг"},
    ]

    result = process_bank_operations(data, ["Перевод", "Оплата", "Возврат"])

    assert result == {
        "Перевод": 2,
        "Оплата": 2,
        "Возврат": 0,
    }


def test_process_bank_operations_empty_data() -> None:
    assert process_bank_operations([], ["Перевод"]) == {"Перевод": 0}
