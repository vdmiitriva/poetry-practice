from unittest.mock import patch

from src.external_api import convert_amount, get_exchange_rate


def test_convert_amount_rub():
    """Проверяет сумму операции в рублях."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "RUB",
            },
        },
    }

    with patch("src.external_api.get_exchange_rate") as mock_rate:
        result = convert_amount(transaction)

    mock_rate.assert_not_called()
    assert result == 100.0


def test_convert_amount_usd():
    """Проверяет конвертацию долларов в рубли."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "USD",
            },
        },
    }

    with patch("src.external_api.get_exchange_rate", return_value=90.0):
        result = convert_amount(transaction)

    assert result == 9000.0


def test_convert_amount_eur():
    """Проверяет конвертацию евро в рубли."""
    transaction = {
        "operationAmount": {
            "amount": "50",
            "currency": {
                "code": "EUR",
            },
        },
    }

    with patch("src.external_api.get_exchange_rate", return_value=100.0):
        result = convert_amount(transaction)

    assert result == 5000.0


def test_get_exchange_rate():
    """Проверяет получение курса валюты через API."""
    response_data = {
        "success": True,
        "rates": {
            "RUB": 90.0,
        },
    }

    with patch("src.external_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = response_data

        result = get_exchange_rate("USD")

    assert result == 90.0
