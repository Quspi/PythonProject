from typing import Iterator, Optional


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Функция, которая принимает на вход данные о транзакциях и возвращает итератор транзакций с указанной валютой."""
    return (item for item in transactions if item["operationAmount"]["currency"]["code"] == currency)


def transaction_descriptions(transactions: list[dict]) -> Iterator[Optional[str]]:
    """Функция-генератор, которая принимает на вход данные о транзакциях
    и возвращает описание транзакций по очереди."""
    for item in transactions:
        yield item.get("description")
