def get_mask_card_number(card_number: int) -> str:
    """Функция, которая принимает на вход номер карты и возвращает
    замаскированный номер в формате XXXX XX** **** XXXX, где видны
    первые 6 и последние 4 цифры, а цифры с 7 по 12 заменены на *."""
    if not isinstance(card_number, int):
        raise TypeError("Номер карты должен быть числом")
    if card_number <= 0:
        raise ValueError("Номер карты должен быть положительным числом")
    if len(str(card_number)) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    card_number_str = str(card_number)
    masked_number = [card_number_str[0:4], card_number_str[4:6] + "**", "****", card_number_str[12:16]]
    return " ".join(masked_number)


def get_mask_account(account_number: int) -> str:
    """Функция, которая принимает на вход номер счета и возвращает
    замаскированный номер в формате **XXXX, где XXXX - это последние 4 цифры."""
    if not isinstance(account_number, int):
        raise TypeError("Номер счета должен быть целым числом")

    if account_number < 0:
        raise ValueError("Номер счета не может быть отрицательным")

    account_number_str = str(account_number)

    if len(account_number_str) < 4:
        raise ValueError("Счет должен содержать не менее 4 цифр")
    return "**" + account_number_str[-4:]
