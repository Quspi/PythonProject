import pytest

from src.widget import get_date, mask_account_card


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


# Тестирование функции get_date
@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-15", "15.03.2024"),
        ("2023-12-31", "31.12.2023"),
        ("2024-01-01", "01.01.2024"),
        ("2000-02-29", "29.02.2000"),
        ("1999-09-09", "09.09.1999"),
    ],
)
def test_valid_dates(date, expected):
    assert get_date(date) == expected


@pytest.mark.parametrize(
    "short_date",
    [
        "",
        "2024-03",
        "24-03-15",
    ],
)
def test_short_strings(short_date):
    with pytest.raises(ValueError):
        get_date(short_date)


@pytest.mark.parametrize(
    "invalid_date",
    [
        "2024/03/15",
        "2024.03.15",
        "2024 03 15",
    ],
)
def test_wrong_separators(invalid_date):
    with pytest.raises(ValueError):
        get_date(invalid_date)


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-15T10:30:00", "15.03.2024"),
        ("2024-03-15T10:30:45.123Z", "15.03.2024"),
        ("2024-03-15 ", "15.03.2024"),
        (" 2024-03-15", "15.03.2024"),
    ],
)
def test_extended_formats(input_date, expected):
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("0001-01-01", "01.01.0001"),
        ("9999-12-31", "31.12.9999"),
    ],
)
def test_extreme_dates(date, expected):
    assert get_date(date) == expected
