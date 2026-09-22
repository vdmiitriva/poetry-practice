def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    return f"{card_number[:4]} " f"{card_number[4:6]}** " f"**** " f"{card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер банковского счёта."""
    if not account_number.isdigit() or len(account_number) < 6:
        raise ValueError("Номер счёта должен содержать 6 и более цифр")
    return f"**{account_number[-4:]}"
