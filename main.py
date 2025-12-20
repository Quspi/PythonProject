import logging
import time
from typing import Optional

from config import CSV_PATH, EXCEL_PATH, JSON_PATH
from src.analysis import filter_by_description
from src.data_loader import read_csv_transactions, read_excel_transactions
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/main.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def show_menu() -> str:
    """Показывает меню и возвращает выбор пользователя."""
    user_choice = input(
        """
Выберите необходимый пункт меню:\n
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
4. Выйти из программы.
"""
    )
    logger.info(f"Выбор в меню: {user_choice}")
    return user_choice


def load_file(choice: str) -> Optional[list[dict]]:
    """Загружает файл с транзакциями в зависимости от выбора"""
    try:
        if choice == "1":
            print("Для обработки выбран JSON-файл.\n")
            logger.info(f"Загрузка файла: {JSON_PATH}")
            return load_transactions(JSON_PATH)
        elif choice == "2":
            print("Для обработки выбран CSV-файл.\n")
            logger.info(f"Загрузка файла: {CSV_PATH}")
            return read_csv_transactions(CSV_PATH, delimiter=";")
        elif choice == "3":
            print("Для обработки выбран EXCEL-файл.\n")
            logger.info(f"Загрузка файла: {EXCEL_PATH}")
            return read_excel_transactions(EXCEL_PATH)
    except ValueError:
        logger.error("Файл не существует или удален.", exc_info=True)
        print("Файл с транзакциями не существует или удален.")

    return None


def get_status() -> str:
    """Запрашивает статус транзакций"""
    print("Введите статус, для фильтрации.")
    while True:
        status = input("Доступные статусы: EXECUTED, CANCELED, PENDING\n").upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            logger.info(f"Для фильтрации выбран статус: {status}")
            print(f"Операции отфильтрованы по статусу '{status}'")
            return status.upper()
        logger.warning(f"Ошибочный ввод статуса для фильтрации: {status}")
        print(f"Статус операции '{status}' недоступен.")


def ask_question(question: str) -> bool:
    """Задает вопрос, ответ на который (Да/Нет)"""
    while True:
        answer = input(f"{question} (Да/Нет)\n").lower()
        if answer == "да":
            logger.info(f"{question} Ввод: {answer}")
            return True
        if answer == "нет":
            logger.info(f"{question} Ввод: {answer}")
            return False
        logger.warning(f"Некорректный ввод: {answer}")
        print("Введите 'Да' или 'Нет'")


def ask_sort_order() -> bool:
    """Спрашивает порядок сортировки."""
    while True:
        order = input("По возрастанию или по убыванию?\n")
        if order.lower() == "по убыванию":
            logger.info(f"Выбран порядок сортировки: {order}")
            return True
        elif order.lower() == "по возрастанию":
            logger.info(f"Выбран порядок сортировки: {order}")
            return False
        logger.warning(f"Некорректный ввод: {order}")
        print("Введите 'по возрастанию' или 'по убыванию'")


def process_transactions(transactions: list[dict], status: str) -> list[dict]:
    filtered_transactions = filter_by_state(transactions, status)

    if ask_question("Отсортировать операции по дате?"):
        logger.info("Выбрана сортировка по дате.")
        reverse = ask_sort_order()
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    if ask_question("Выводить только рублевые транзакции?"):
        logger.info("Выбрана сортировка по рублевым транзакциям.")
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    if ask_question("Отфильтровать список транзакций по определенному слову в описании?"):
        logger.info("Выбрана сортировка по ключевому слову.")
        search_string = input("Введите слово для поиска:\n")
        logger.info(f"Строка для поиска в описании: {search_string}")
        filtered_transactions = filter_by_description(filtered_transactions, search_string)

    return filtered_transactions


def print_transactions(transactions: list[dict]) -> None:
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        logger.info("Не найдено транзакций подходящих под условия фильтрации.")
        return None

    print("Распечатываю итоговый список транзакций...")
    time.sleep(1)
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    time.sleep(1)

    desc_gen = transaction_descriptions(transactions)

    for transaction in transactions:
        date = get_date(transaction["date"])
        description = next(desc_gen)

        try:
            from_ = mask_account_card(transaction["from"])
        except (ValueError, TypeError):
            from_ = None

        try:
            to = mask_account_card(transaction["to"])
        except ValueError:
            logger.error("Номер карты или аккаунта неверного формата.", exc_info=True)
            continue

        if "operationAmount" in transaction:
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["code"]
        else:
            amount = transaction["amount"]
            currency = transaction["currency_code"]

        if from_:
            print(f"{date} {description}\n{from_} -> {to}\nСумма: {amount} {currency}\n")
        else:
            print(f"{date} {description}\n{to}\nСумма: {amount} {currency}\n")


def main() -> None:
    print("Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        choice = show_menu()

        if choice == "4":
            logger.info("Пользователь завершил работу программы.")
            print("Программа завершила работу.")
            break

        transactions = load_file(choice)
        logger.info(f"Загружено {len(transactions) if transactions else 0} транзакций")

        if transactions is None:
            logger.warning(f"Ошибочный ввод в меню: {choice}")
            print("Выбран некорректный пункт меню, повторите ввод:")
            continue

        status = get_status()

        filtered_transactions = process_transactions(transactions, status)
        logger.info(f"Отфильтровано {len(filtered_transactions)} транзакций.")

        print_transactions(filtered_transactions)
        time.sleep(3)


if __name__ == "__main__":
    main()
