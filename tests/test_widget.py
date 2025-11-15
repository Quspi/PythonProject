import pytest

from src.widget import mask_account_card


# Тестирование функции mask_account_card
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("Card 1111111111111111", "Card 1111 11** **** 1111"),
    ],
)
def test_valid_mask_card(card_number, expected):
    assert mask_account_card(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("счет 12345678", "счет **5678"),
        ("СЧЕТ 1234", "СЧЕТ **1234"),
        ("Счет 10000000000000000000", "Счет **0000"),
    ],
)
def test_valid_mask_account(account_number, expected):
    assert mask_account_card(account_number) == expected


@pytest.mark.parametrize(
    "card_number, expected_error",
    [
        ("Карта 1234", ValueError),
        ("Карта 1234567890", ValueError),
        ("Карта 12345678901234567890", ValueError),
        ("Карта 0000000000000000", ValueError),
    ],
)
def test_invalid_mask_card(card_number, expected_error):
    with pytest.raises(expected_error):
        mask_account_card(card_number)


@pytest.mark.parametrize(
    "account_number, expected_error",
    [
        ("Счет 123", ValueError),
        ("Счет 12", ValueError),
        ("Счет 1", ValueError),
        ("Счет 0", ValueError),
    ],
)
def test_invalid_mask_account(account_number, expected_error):
    with pytest.raises(expected_error):
        mask_account_card(account_number)


@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        ("", ValueError),
        ("Счет", ValueError),
        ("Карта", ValueError),
        ("Счет abcdef", ValueError),
        ("Карта 12abc456def789", ValueError),
        (None, TypeError),
        (123, TypeError),
    ],
)
def test_invalid_input_types(invalid_input, expected_error):
    with pytest.raises(expected_error):
        mask_account_card(invalid_input)


@pytest.mark.parametrize(
    "special_format, expected",
    [
        ("Счет №12345678901234567890", "Счет № **7890"),
        ("Карта: 1234567890123456", "Карта: 1234 56** **** 3456"),
        ("Visa 1234 5678 9012 3456", "Visa 1234 56** **** 3456"),
    ],
)
def test_special_formats(special_format, expected):
    assert mask_account_card(special_format) == expected
