import pytest

from src.mask import get_mask_card_number


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
