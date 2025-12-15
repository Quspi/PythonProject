import logging

from src.mask import get_mask_account, get_mask_card_number

logger = logging.getLogger("widget")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/widget.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


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

    if "счет" in account_clean.lower():
        mask = get_mask_account(int(number))
        result = f"{account_clean} {mask}"
        logger.info(f"Успешно: тип {account_clean}, результат: '{result}'")
        return result
    else:
        mask = get_mask_card_number(int(number))
        result = f"{account_clean} {mask}"
        logger.info(f"Успешно: тип {account_clean}, результат: '{result}'")
        return result


def get_date(data: str) -> str:
    """Функция, которая преобразует дату из ISO формата в формат ДД.ММ.ГГГГ."""
    logger.info(f"Преобразование даты: '{data}'")
    data = data.strip()

    if len(data) < 10:
        logger.error(f"Слишком короткая строка: '{data}'")
        raise ValueError("Строка слишком короткая для даты в формате ГГГГ-ММ-ДД")
    if data[4] != "-" or data[7] != "-":
        logger.error(f"Ошибка: неверный формат даты '{data}'")
        raise ValueError("Неверный формат даты. Ожидается: ГГГГ-ММ-ДД")

    result = f"{data[8:10]}.{data[5:7]}.{data[0:4]}"
    logger.info(f"Успешно: '{data}' -> '{result}'")
    return result
