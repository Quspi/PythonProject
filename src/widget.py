from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция, которая маскирует номер банковской карты или счета."""
    account = ""
    number = ""
    for symbol in account_card:
        if symbol.isdigit():
            number += symbol
        else:
            account += symbol

    account_clean = account.strip()

    if account_clean.lower() == "счет":
        mask = get_mask_account(int(number))
        return f"{account_clean} {mask}"
    else:
        mask = get_mask_card_number(int(number))
        return f"{account_clean} {mask}"


def get_date(data: str) -> str:
    """Функция, которая преобразует дату из ISO формата в формат ДД.ММ.ГГГГ."""
    return f"{data[8:10]}.{data[5:7]}.{data[0:4]}"
