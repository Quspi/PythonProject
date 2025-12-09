import json
import os


def load_transactions(file_path: str) -> list[dict]:
    """Загружает транзакции из JSON файла."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="UTF-8") as file:
        try:
            transactions = json.load(file)

        except json.decoder.JSONDecodeError:
            return []

    if not isinstance(transactions, list):
        return []

    return transactions
