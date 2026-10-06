import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("API_KEY is not set")


def get_exchange_rate(currency: str) -> float:
    """Получает курс валюты к рублю через внешний API."""
    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {
        "apikey": API_KEY,
    }

    params = {
        "base": currency,
        "symbols": "RUB",
    }

    response = requests.get(url, headers=headers, params=params)

    return float(response.json()["rates"]["RUB"])


def convert_amount(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    rate = get_exchange_rate(currency)

    return amount * rate
