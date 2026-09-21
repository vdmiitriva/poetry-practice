import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations():
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
def test_filter_by_state(operations, state, expected_count):
    result = filter_by_state(operations, state)
    assert len(result) == expected_count


def test_filter_by_state_without_state():
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
def test_sort_by_date(operations, reverse):
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


def test_sort_by_date_same_dates():
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


def test_sort_by_date_different_formats():
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


def test_sort_by_date_invalid_date():
    data = [
        {"date": "2024-03-15"},
        {"date": "не дата"},
    ]

    with pytest.raises(ValueError):
        sort_by_date(data)
