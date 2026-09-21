import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1234123412341234", "1234 12** **** 1234"),
        ("1111111111111111", "1111 11** **** 1111"),
        ("0987098709870987", "0987 09** **** 0987"),
    ],
)
def test_get_mask_card_number(number: str, expected: str) -> None:
    assert get_mask_card_number(number) == expected


@pytest.mark.parametrize("number", ["12341234123", "1234123412341", "", "1234abcd12345678"])
def test_get_mask_card_number_invalid(number: str) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(number)


@pytest.mark.parametrize("number, expected", [("123456", "**3456"), ("1234567890", "**7890"), ("11111111", "**1111")])
def test_get_mask_account(number: str, expected: str) -> None:
    assert get_mask_account(number) == expected


@pytest.mark.parametrize("number", ["123", "", "12345", "1234567ab"])
def test_get_mask_account_invalid(number: str) -> None:
    with pytest.raises(ValueError):
        get_mask_account(number)
