import logging
from typing import Union

import pandas as pd

logger = logging.getLogger("data_loader")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/data_loader.log", "w", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_csv_transactions(filepath: str, delimiter: str = ",") -> list[dict]:
    """Загружает транзакции из CSV файла и возвращает их в формате list[dict]"""
    try:
        transactions = pd.read_csv(filepath, delimiter=delimiter)

        result = transactions.to_dict(orient="records")
        logger.info(f"{len(result)} транзакций успешно загружено из файла: {filepath}")

        return result

    except FileNotFoundError as error:
        logger.error(f"Ошибка: {error}: Файл не существует или удален.")
        raise ValueError(f"Файл не найден {filepath}")


def read_excel_transactions(filepath: str, sheet_name: Union[str, int] = 0) -> list[dict]:
    """Загружает транзакции из Excel файла и возвращает их в формате list[dict]"""
    try:
        transactions = pd.read_excel(filepath, sheet_name=sheet_name)

        result = transactions.to_dict(orient="records")
        logger.info(f"{len(result)} транзакций успешно загружено из файла: {filepath}")

        return result

    except FileNotFoundError as error:
        logger.error(f"Ошибка: {error}: Файл не существует или удален.")
        raise ValueError(f"Файл не найден {filepath}")
