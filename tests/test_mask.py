import pytest

from src.mask import get_mask_account, get_mask_card_number


# Тестирование функции get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
        (9999888877776666, "9999 88** **** 6666"),
        (1000000000000000, "1000 00** **** 0000"),
        (9999999999999999, "9999 99** **** 9999"),
    ],
)
def test_valid_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("card_number", [12345, 11112, 99998888777766661233, 100000000000000031312])
def test_invalid_length_mask_card_number(card_number):
    with pytest.raises(ValueError) as error:
        get_mask_card_number(card_number)
    assert str(error.value) == "Номер карты должен содержать 16 цифр"


@pytest.mark.parametrize(
    "invalid_number, expected_error",
    [
        ("9999999999999999", TypeError),
        (None, TypeError),
        ([], TypeError),
        ({}, TypeError),
        (-1234567890123456, ValueError),
        (1234567890123456.0, TypeError),
    ],
)
def test_invalid_input_mask_card_number(invalid_number, expected_error):
    with pytest.raises(expected_error):
        get_mask_card_number(invalid_number)


def test_zero_mask_card_number():
    with pytest.raises(ValueError) as error:
        get_mask_card_number(0)
    assert str(error.value) == "Номер карты должен быть положительным числом"


# Тестирование функции get_mask_account
@pytest.mark.parametrize(
    "account, expected",
    [
        (12345678901234567890, "**7890"),
        (123456, "**3456"),
        (9999, "**9999"),
        (10000000000000000000, "**0000"),
        (99999999999999999999, "**9999"),
        (12121212121212121212121212, "**1212"),
        (11111111111111111111, "**1111"),
        (1234123412341234, "**1234"),
    ],
)
def test_valid_mask_account(account, expected):
    assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account, expected_error",
    [(1, ValueError), (12, ValueError), (123, ValueError), (0000, ValueError), (0, ValueError)],
)
def test_invalid_length_mask_account(account, expected_error):
    with pytest.raises(expected_error) as error:
        get_mask_account(account)
    assert str(error.value) == "Счет должен содержать не менее 4 цифр"


@pytest.mark.parametrize(
    "account, expected_error",
    [
        ("", TypeError),
        (None, TypeError),
        ([], TypeError),
        ({}, TypeError),
        ((), TypeError),
        (123.45, TypeError),
        ("123124", TypeError),
    ],
)
def test_wrong_type_mask_account(account, expected_error):
    with pytest.raises(expected_error) as error:
        get_mask_account(account)
    assert str(error.value) == "Номер счета должен быть целым числом"


@pytest.mark.parametrize(
    "account, expected_error", [(-1234, ValueError), (-123, ValueError), (-1, ValueError), (-9999, ValueError)]
)
def test_negative_numbers_mask_account(account, expected_error):
    with pytest.raises(expected_error) as error:
        get_mask_account(account)
    assert str(error.value) == "Номер счета не может быть отрицательным"
