def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    return f"{card_number[:4]} " f"{card_number[4:6]}** " f"**** " f"{card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер банковского счёта."""
    return f"**{account_number[-4:]}"
