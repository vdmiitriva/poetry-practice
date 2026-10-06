import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(
    logs_dir / "utils.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_operations(file_path):
    """Загружает список операций из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info(
                "Операции успешно загружены из файла %s",
                file_path,
            )
            return data

        logger.error("JSON-файл должен содержать список операций")
        return []

    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []

    except json.JSONDecodeError:
        logger.error("Некорректный JSON в файле: %s", file_path)
        return []
