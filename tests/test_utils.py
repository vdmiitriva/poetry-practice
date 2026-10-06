import json
from unittest.mock import mock_open, patch

from src.utils import load_operations


def test_load_operations_succes():
    """Проверяет успешное чтение JSON-файла."""
    data = [{"id": 1}, {"id": 2}]

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = load_operations("operations.json")

    assert result == data


def test_load_operations_empty_file():
    """Проверяет чтение пустого JSON-файла."""
    with patch("builtins.open", mock_open(read_data="")):
        result = load_operations("operations.json")

    assert result == []


def test_load_operations_not_list():
    """Проверяет обработку JSON, содержащего не список."""
    data = {"id": 1}

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = load_operations("operations.json")

    assert result == []


def test_load_operations_file_not_found():
    """Проверяет обработку отсутствующего файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_operations("operations.json")

    assert result == []


def test_load_operations_invalid_json():
    """Проверяет обработку некорректного JSON."""
    with patch("builtins.open", mock_open(read_data="{invalid json")):
        result = load_operations("operations.json")

    assert result == []
