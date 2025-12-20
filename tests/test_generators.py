from typing import Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тестирование функции filter_by_currency
@pytest.mark.parametrize("currency", [("RUB"), ("USD"), ("EUR")])
def test_filter_by_currency(sample_transactions, currency):
    result = filter_by_currency(sample_transactions, currency)
    expected = [item for item in sample_transactions if item["operationAmount"]["currency"]["code"] == currency]
    assert list(result) == expected


@pytest.mark.parametrize("currency", [("RUB"), ("USD"), ("EUR")])
def test_filter_by_currency_csv_xlsx(sample_transactions_csv_xlsx, currency):
    result = filter_by_currency(sample_transactions_csv_xlsx, currency)
    expected = [item for item in sample_transactions_csv_xlsx if item["currency_code"] == currency]
    assert list(result) == expected


def test_empty_filter_by_currency(empty_transactions):
    result = filter_by_currency(empty_transactions, "USD")
    expected = []
    assert list(result) == expected


def test_all_match(usd_only_transactions):
    result = filter_by_currency(usd_only_transactions, "USD")
    expected = [item for item in usd_only_transactions if item["operationAmount"]["currency"]["code"] == "USD"]
    assert list(result) == expected


def test_type_filter_by_currency(usd_only_transactions):
    result = filter_by_currency(usd_only_transactions, "USD")
    assert isinstance(result, Iterator)


def test_no_matches(usd_only_transactions):
    result = filter_by_currency(usd_only_transactions, "RUB")
    expected = []
    assert list(result) == expected


def test_invalid_structure_transactions(invalid_structure_transactions):
    result = filter_by_currency(invalid_structure_transactions, "RUB")
    with pytest.raises(KeyError):
        list(result)


# Тестирование функции-генератора transaction_descriptions


def test_transaction_descriptions(transactions_with_descriptions):
    gen = transaction_descriptions(transactions_with_descriptions)
    assert isinstance(gen, Iterator)
    assert next(gen) == "Payment"
    assert next(gen) == "Transfer"
    assert next(gen) == "Withdrawal"

    with pytest.raises(StopIteration):
        next(gen)


def test_transactions_without_descriptions(transactions_without_descriptions):
    gen = transaction_descriptions(transactions_without_descriptions)
    assert isinstance(gen, Iterator)
    assert next(gen) is None
    assert next(gen) is None
    assert next(gen) is None

    with pytest.raises(StopIteration):
        next(gen)


def test_transactions_mixed_descriptions(transactions_mixed_descriptions):
    gen = transaction_descriptions(transactions_mixed_descriptions)
    assert isinstance(gen, Iterator)
    assert next(gen) == "Payment"
    assert next(gen) is None
    assert next(gen) == ""
    assert next(gen) is None

    with pytest.raises(StopIteration):
        next(gen)


def test_transactions_long_description(transactions_long_description):
    gen = transaction_descriptions(transactions_long_description)
    assert isinstance(gen, Iterator)
    assert next(gen) == "A" * 1000

    with pytest.raises(StopIteration):
        next(gen)


def test_empty_list(empty_transactions):
    gen = transaction_descriptions(empty_transactions)
    assert isinstance(gen, Iterator)
    assert list(gen) == []


# Тестирование функции-генератора card_number_generator


def test_card_number_generator():
    gen = card_number_generator(1, 3)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(gen)


def test_one_card_number():
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    with pytest.raises(StopIteration):
        next(gen)


def test_invalid_start_stop():
    gen = card_number_generator(5, 3)
    assert list(gen) == []


def test_large_numbers():
    gen = card_number_generator(9999999999999998, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9998"
    assert next(gen) == "9999 9999 9999 9999"

    with pytest.raises(StopIteration):
        next(gen)


def test_boundary_transition():
    gen = card_number_generator(9999, 10000)
    assert next(gen) == "0000 0000 0000 9999"
    assert next(gen) == "0000 0000 0001 0000"

    with pytest.raises(StopIteration):
        next(gen)


def test_format():
    gen = card_number_generator(9999, 9999)
    card_number = next(gen)
    assert len(card_number) == 19
    assert card_number.count(" ") == 3
    assert card_number.replace(" ", "").isdigit()


def test_negative_numbers():
    gen = card_number_generator(-1, 5)
    with pytest.raises(ValueError) as e:
        next(gen)
    assert str(e.value) == "Числа должны быть в диапазоне от 0 до 9999999999999999"


def test_too_large_numbers():
    gen = card_number_generator(1, 10000000000000000)
    with pytest.raises(ValueError) as e:
        next(gen)
    assert str(e.value) == "Числа должны быть в диапазоне от 0 до 9999999999999999"
