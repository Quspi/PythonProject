from typing import Iterator

import pytest

from src.generators import filter_by_currency


@pytest.mark.parametrize("currency", [("RUB"), ("USD"), ("EUR")])
def test_filter_by_currency(sample_transactions, currency):
    result = filter_by_currency(sample_transactions, currency)
    expected = [item for item in sample_transactions if item["operationAmount"]["currency"]["code"] == currency]
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
