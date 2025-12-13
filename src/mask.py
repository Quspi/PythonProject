import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("mask")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/mask.log", "w", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_mask_card_number(card_number: int) -> str:
    """Функция, которая принимает на вход номер карты и возвращает
    замаскированный номер в формате XXXX XX** **** XXXX, где видны
    первые 6 и последние 4 цифры, а цифры с 7 по 12 заменены на *."""
    if not isinstance(card_number, int):
        logger.error(f"Номер карты должен быть int, получен: {type(card_number).__name__}")
        raise TypeError("Номер карты должен быть числом")
    if card_number <= 0:
        logger.error(f"Номер карты должен быть > 0, получен: {card_number}")
        raise ValueError("Номер карты должен быть положительным числом")
    if len(str(card_number)) != 16:
        logger.error(f"Длинна номера должна быть == 16, получено: {len(str(card_number))}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    card_number_str = str(card_number)
    masked_number = [card_number_str[0:4], card_number_str[4:6] + "**", "****", card_number_str[12:16]]
    result = " ".join(masked_number)

    logger.info(f"Номер карты успешно замаскирован. Результат: {result}")

    return result


def get_mask_account(account_number: int) -> str:
    """Функция, которая принимает на вход номер счета и возвращает
    замаскированный номер в формате **XXXX, где XXXX - это последние 4 цифры."""
    if not isinstance(account_number, int):
        logger.error(f"Номер счета должен быть int, получен: {type(account_number).__name__}")
        raise TypeError("Номер счета должен быть целым числом")

    if account_number < 0:
        logger.error(f"Номер счета должен быть > 0, получен: {account_number}")
        raise ValueError("Номер счета не может быть отрицательным")

    account_number_str = str(account_number)

    if len(account_number_str) < 4:
        logger.error(f"Длинна счета должна > 4, получено: {len(account_number_str)}")
        raise ValueError("Счет должен содержать не менее 4 цифр")

    result = "**" + account_number_str[-4:]

    logger.info(f"Номер счета успешно замаскирован. Результат: {result}")

    return result
