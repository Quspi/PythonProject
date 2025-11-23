from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Функция, которая принимает на вход данные о транзакциях и возвращает итератор транзакций с указанной валютой"""
    return (item for item in transactions if item["operationAmount"]["currency"]["code"] == currency)
