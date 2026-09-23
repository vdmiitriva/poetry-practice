from src.generators import filter_by_currency


def test_filter_by_currency_usd(transactions):
    result = list(filter_by_currency(transactions, "USD"))

    assert len(result) == 3
    assert all(
        transaction["operationAmount"]["currency"]["code"] == "USD"
        for transaction in result
    )


def test_filter_by_currency_no_matches(transactions):
    result = list(filter_by_currency(transactions, "EUR"))

    assert result == []


def test_filter_by_currency_empty_list():
    result = list(filter_by_currency([], "USD"))

    assert result == []