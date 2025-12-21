import json
import logging
import os

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/utils.log", "w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_transactions(file_path: str) -> list[dict]:
    """Загружает транзакции из JSON файла."""
    file_name = os.path.basename(file_path)

    if not os.path.exists(file_path):
        logger.warning(f"Путь: {file_path} не существует.")
        return []

    with open(file_path, "r", encoding="UTF-8") as file:
        logger.info(f"Открыт файл: {file_name}")
        try:
            transactions = json.load(file)
            logger.info(f"Файл {file_name} загружен, {len(transactions)} транзакций")

        except json.decoder.JSONDecodeError as error:
            logger.error(f"Ошибка декодирования JSON: {error} Файл: {file_name}")
            return []

    if not isinstance(transactions, list):
        logger.warning(
            f"Файл {file_name} содержит неверную структуру. Ожидается: list, получен {type(transactions).__name__}"
        )
        return []

    return transactions
