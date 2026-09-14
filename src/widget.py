from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(s: str) -> str:
    parts = s.split()
    if len(parts) < 2:
        return ""

    name = " ".join(parts[:-1])
    number = parts[-1]

    if name == "Счет":
        return f"{name} {get_mask_account(number)}"
    return f"{name} {get_mask_card_number(number)}"


def get_date(s: str) -> str:
    date = datetime.fromisoformat(s)
    return date.strftime("%d.%m.%Y")
