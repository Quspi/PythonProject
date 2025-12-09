import os

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_transaction_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли. Поддерживает RUB, USD, EUR. Для конвертации использует внешнее API."""
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]
    except KeyError:
        raise KeyError("Некорректный формат данных")

    if currency == "RUB":
        return amount

    elif currency in ("EUR", "USD"):
        url = "https://api.apilayer.com/exchangerates_data/convert"
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise ValueError("API_KEY не найден в переменных окружения")

        headers = {"apikey": api_key}
        params = {"to": "RUB", "from": currency, "amount": amount}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()
                return round(float(data["result"]), 2)
            elif 400 <= response.status_code < 500:
                raise ValueError(f"Код ошибки: {response.status_code}")
            elif 500 <= response.status_code < 600:
                raise ConnectionError(f"Код ошибки: {response.status_code}")
            else:
                raise ConnectionError(f"Код ошибки: {response.status_code}")

        except requests.exceptions.RequestException as error:
            raise ConnectionError(f"Ошибка сети: {error}")

    else:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")
