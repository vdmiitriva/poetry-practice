import json

import pandas as pd

from src.utils import load_operations, load_operations_from_csv, load_operations_from_excel


def test_load_operations_success(tmp_path):
    file_path = tmp_path / "operations.json"
    operations = [{"id": 1, "amount": 100}]

    file_path.write_text(
        json.dumps(operations),
        encoding="utf-8",
    )

    result = load_operations(file_path)

    assert result == operations


def test_load_operations_file_not_found(tmp_path):
    file_path = tmp_path / "missing.json"

    result = load_operations(file_path)

    assert result == []


def test_load_operations_invalid_json(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text("invalid json", encoding="utf-8")

    result = load_operations(file_path)

    assert result == []


def test_load_operations_not_a_list(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text(
        json.dumps({"id": 1}),
        encoding="utf-8",
    )

    result = load_operations(file_path)

    assert result == []


def test_load_operations_from_csv_success(tmp_path):
    file_path = tmp_path / "operations.csv"
    file_path.write_text(
        "id;amount;currency_code\n1;100;RUB\n",
        encoding="utf-8",
    )

    result = load_operations_from_csv(file_path)

    assert result == [{"id": 1, "amount": 100, "currency_code": "RUB"}]


def test_load_operations_from_csv_file_not_found(tmp_path):
    file_path = tmp_path / "missing.csv"

    result = load_operations_from_csv(file_path)

    assert result == []


def test_load_operations_from_excel_success(tmp_path):
    file_path = tmp_path / "operations.xlsx"
    operations = [{"id": 1, "amount": 100, "currency_code": "RUB"}]

    pd.DataFrame(operations).to_excel(file_path, index=False)

    result = load_operations_from_excel(file_path)

    assert result == operations


def test_load_operations_from_excel_file_not_found(tmp_path):
    file_path = tmp_path / "missing.xlsx"

    result = load_operations_from_excel(file_path)

    assert result == []
