import json
from typing import Any


def load_operations(file_path: str) -> list[dict[str, Any]]:
    """Читает данные о финансовых операциях из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except FileNotFoundError, json.JSONDecodeError:
        return []
