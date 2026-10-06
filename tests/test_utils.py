import json

from src.utils import load_operations


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
