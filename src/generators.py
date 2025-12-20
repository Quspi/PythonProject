import logging
from typing import Generator, Iterator, Optional

logger = logging.getLogger("generators")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/generators.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Функция, которая принимает на вход данные о транзакциях и возвращает итератор транзакций с указанной валютой."""
    logger.info(f"Вызвана с: transactions={len(transactions)}, currency={currency}")
    if transactions and "operationAmount" in transactions[0]:
        return (item for item in transactions if item["operationAmount"]["currency"]["code"] == currency)
    else:
        return (item for item in transactions if item["currency_code"] == currency)


def transaction_descriptions(transactions: list[dict]) -> Iterator[Optional[str]]:
    """Функция-генератор, которая принимает на вход данные о транзакциях
    и возвращает описание транзакций по очереди."""
    logger.info(f"Запуск извлечения описаний ({len(transactions)} транзакций)")
    for item in transactions:
        yield item.get("description")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генерирует номера карт в формате "XXXX XXXX XXXX XXXX" в диапазоне от start до stop."""
    logger.info(f"Запуск генерации номеров карт: start={start}, stop={stop} (всего: {stop - start + 1} номеров)")
    if start < 0 or stop < 0 or len(str(start)) > 16 or len(str(stop)) > 16:
        logger.error(f"Числа должны быть в диапазоне от 0 до 9999999999999999, получено: start={start} stop={stop}")
        raise ValueError("Числа должны быть в диапазоне от 0 до 9999999999999999")
    else:
        for number in range(start, stop + 1):
            card_number_str = str(number).zfill(16)
            formated_card_number = " ".join([card_number_str[i : i + 4] for i in range(0, 16, 4)])
            yield formated_card_number
