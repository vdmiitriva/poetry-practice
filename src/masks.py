import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(
    "logs/masks.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


file_handler = logging.FileHandler(
    logs_dir / "masks.log",
    mode="w",
    encoding="utf-8",
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    if not card_number.isdigit() or len(card_number) != 16:
        logger.error("Номер карты должен содержать 16 цифр")
        raise ValueError("Номер карты должен содержать 16 цифр")

    logger.info("Номер карты успешно замаскирован")
    return f"{card_number[:4]} " f"{card_number[4:6]}** " f"**** " f"{card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер банковского счёта."""
    if not account_number.isdigit() or len(account_number) < 6:
        logger.error("Номер счёта должен содержать 6 и более цифр")
        raise ValueError("Номер счёта должен содержать 6 и более цифр")

    logger.info("Номер счёта успешно замаскирован")
    return f"**{account_number[-4:]}"
