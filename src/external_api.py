import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("external_api")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/external_api.log", "w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


def convert_transaction_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли. Поддерживает RUB, USD, EUR. Для конвертации использует внешнее API."""
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]
        logger.info(f"Успешно получены amount:{amount}, currency:{currency}")
    except KeyError as error:
        logger.error(f"Ошибка: {error}, входные данные: {transaction}", exc_info=True)
        raise KeyError("Некорректный формат данных")

    if currency == "RUB":
        return amount

    elif currency in ("EUR", "USD"):
        url = "https://api.apilayer.com/exchangerates_data/convert"
        api_key = os.getenv("API_KEY")

        if not api_key:
            logger.error("Ошибка: ValueError, API_KEY не найден в переменных окружения")
            raise ValueError("API_KEY не найден в переменных окружения")

        headers = {"apikey": api_key}
        params = {"to": "RUB", "from": currency, "amount": amount}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            logger.info(f"Отправлен GET запрос: URL: {url}, headers: apikey, params: {params}")
            if response.status_code == 200:
                data = response.json()
                result = round(float(data["result"]), 2)
                logger.info(f"Успешный API запрос, результат для {currency}{amount}: RUB{result}")
                return result
            elif 400 <= response.status_code < 500:
                logger.error(f"Клиентская ошибка API {response.status_code}: {response.text}")
                raise ValueError(f"Код ошибки: {response.status_code}")
            elif 500 <= response.status_code < 600:
                logger.error(f"Серверная ошибка API: {response.status_code} - {response.text}")
                raise ConnectionError(f"Код ошибки: {response.status_code}")
            else:
                logger.error(f"Неудачный API запрос! Код ошибки: {response.status_code}")
                raise ConnectionError(f"Код ошибки: {response.status_code}")

        except requests.exceptions.RequestException as error:
            logger.error(f"Ошибка сети! {error}", exc_info=True)
            raise ConnectionError(f"Ошибка сети: {error}")

    else:
        logger.error(f"Неподдерживаемая валюта: {currency}")
        raise ValueError(f"Неподдерживаемая валюта: {currency}")
