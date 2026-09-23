import pytest


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
        },
        {
            "id": 594226727,
            "operationAmount": {
                "currency": {
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
        },
    ]