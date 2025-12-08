# Виджет банковских операций клиента

***Учебный проект в процессе разработки***

Проект создается в рамках обучения Python и представляет собой систему для обработки банковских операций. 
На текущем этапе реализуются базовые функции работы с финансовыми данными.

## Оглавление

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка](#установка)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Разработка](#разработка)
- [Лицензия](#лицензия)
- [Автор](#автор)

## Технологии
- Python 3.12.7
- Poetry (управление зависимостями)
- Black (форматирование кода)
- Flake8 (стиль кода)
- Pytest (тестирование)
- Requests (HTTP-запросы)
- python-dotenv (переменные окружения)

## Функциональность

### Реализовано
- Маскировка номеров банковских карт
- Маскировка номеров счетов
- Фильтрация операций по статусу
- Сортировка операций по дате
- Форматирование дат
- Фильтрация операций по валюте
- Генерация номеров банковских карт
- Извлечение описаний транзакций
- Логирование данных в консоль или файл
- Загрузка транзакций из JSON файлов
- Конвертация сумм транзакций в рубли через внешний API (Поддержка валют: USD, EUR)

## Установка

```
# Клонирование репозитория
git clone <repository-url>

# Установка зависимостей
poetry install

# Активация окружения
poetry self add poetry-plugin-shell
poetry shell

# Настройка переменных окружения для работы с API
Создайте файл .env в корне проекта:
API_KEY=ваш_ключ_от_apilayer.com (получить на https://apilayer.com/)
```

## Использование
### Функции
```python
from src.mask import get_mask_card_number, get_mask_account
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.widget import mask_account_card, get_date
from src.utils import load_transactions
from src.external_api import convert_transaction_to_rub

# Маскировка карты
get_mask_card_number(7000792289606361)
# 7000 79** **** 6361

# Маскировка счета
get_mask_account(73654108430135874305)
# **4305

# Универсальная маскировка
mask_account_card("Visa Platinum 7000792289606361")
# Visa Platinum 7000 79** **** 6361

mask_account_card("Счет 73654108430135874305")
# Счет **4305

# Фильтрация по статусу
operations = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
filter_by_state(operations, "EXECUTED")
# [{'id': 1, 'state': 'EXECUTED'}]

# Сортировка по дате
dates = [{"id": 1, "date": "2024-01-01"}, {"id": 2, "date": "2024-03-01"}, {"id": 3, "date": "2024-02-01"}]
sort_by_date(dates)
# [{'id': 2, 'date': '2024-03-01'}, {'id': 3, 'date': '2024-02-01'}, {'id': 1, 'date': '2024-01-01'}]

# Фильтрация по валюте
transactions = [{"id": 1, "operationAmount": {"currency": {"code": "USD"}}}]
list(filter_by_currency(transactions, "USD"))
# [{'id': 1, 'operationAmount': {'currency': {'code': 'USD'}}}]

# Описания транзакций
transactions = [{"description": "Оплата товара"}, {"description": "Перевод организации"}]
list(transaction_descriptions(transactions))
# ['Оплата товара', 'Перевод организации']

# Генерация номеров карт
list(card_number_generator(1, 3))
# ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']

# Форматирование даты
get_date("2024-03-14T10:30:00")
# 14.03.2024

# Загрузка транзакций
transactions = load_transactions("data/operations.json")

# Конвертация в рубли
transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
converted_amount = convert_transaction_to_rub(transaction)
# 9300.50 (пример конвертации 100 USD в RUB)

# Конвертация в рубли с обработкой ошибок
try:
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    converted_amount = convert_transaction_to_rub(transaction)
    # 9300.50 (пример конвертации 100 USD в RUB)
except ValueError as e:
    print(f"Ошибка данных: {e}")
except ConnectionError as e:
    print(f"Ошибка сети: {e}")

```
### Декораторы
```python
from src.decorators import log

# Логирование в консоль
@log()
def add(a, b):
    return a + b

add(2, 3)
# add ok: 5

# Логирование в файл
@log("operations.log")
def process_data(data):
    return len(data)

process_data([1, 2, 3])
# запись в файл logs/operations.log: "process_data ok: 3"

# Логирование ошибок
@log()
def risky_operation(x):
    if x < 0:
        raise ValueError("Negative value not allowed")
    return x * 2

risky_operation(-5)
# risky_operation ValueError: Negative value not allowed. Inputs: (-5,), {}
```
## Разработка
Проект находится на стадии активного обучения и развития. Кодовая база постоянно улучшается, добавляется новая функциональность и исправляются ошибки.

## Тестирование

Проект покрыт юнит-тестами Pytest. Для их запуска выполните команды:
```
# Запуск всех тестов
pytest

# Запуск с отчетом о покрытии в консоли
pytest --cov=src

# Генерация HTML отчета о покрытии (будет создана папка htmlcov/)
pytest --cov=src --cov-report=html
```

## Лицензия
Этот проект распространяется под лицензией MIT.

## Автор
**Oleg Tamanov**

Email: olegtamanov@gmail.com
