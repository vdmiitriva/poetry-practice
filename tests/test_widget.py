import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "Visa Classic 1234123412341234",
            "Visa Classic 1234 12** **** 1234",
        ),
        (
            "MasterCard 1111111111111111",
            "MasterCard 1111 11** **** 1111",
        ),
        (
            "Счет 1234567890",
            "Счет **7890",
        ),
        (
            "Счет 123456",
            "Счет **3456",
        ),
        (
            "Visa Classic 1234567890123456",
            "Visa Classic 1234 56** **** 3456",
        ),
        (
            "Счет 123456789",
            "Счет **6789",
        ),
    ],
)
def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "Visa",
        "Счёт",
    ],
)
def test_mask_account_card_empty(value):
    assert mask_account_card(value) == ""


@pytest.mark.parametrize(
    "value",
    [
        "Visa Classic 123",
        "MasterCard 12345",
        "Счет 123",
    ],
)
def test_mask_account_card_invalid_number(value):
    with pytest.raises(ValueError):
        mask_account_card(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2023-08-15T12:30:45", "15.08.2023"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-12-31T23:59:59", "31.12.2024"),
        ("2024-02-29T12:00:00", "29.02.2024"),
        ("2024-02-29", "29.02.2024"),
        ("2023-01-01", "01.01.2023"),
    ],
)
def test_get_date(value, expected):
    assert get_date(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "не дата",
        "2024-99-99",
        "2024-02-30",
        "15.08.2024",
    ],
)
def test_get_date_invalid(value):
    with pytest.raises(ValueError):
        get_date(value)
