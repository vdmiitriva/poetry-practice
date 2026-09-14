from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(s: str) -> str:
    parts = s.split()

    name = ' .'.join(parts[:-1])
    number = parts[-1]

    if name == 'Счет':
        return f"{name} {get_mask_account(number)}"
    return f"{name} {get_mask_card_number(number)}"



