# Система обработки банковских транзакций

Учебный проект для освоения работы с финансовыми данными, модульной архитектурой и тестированием в Python.

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![Tests](https://img.shields.io/badge/tests-100%25_passing-success)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Оглавление

- *[Технологии](#технологии)*
- *[Функциональность](#функциональность)*
- *[Поддерживаемые форматы данных](#поддерживаемые-форматы-данных)*
- *[Логирование](#логирование)*
- *[Установка](#установка)*
- *[Использование](#использование)*
- *[Запуск приложения](#запуск-приложения)*
- *[Разработка](#разработка)*
- *[Тестирование](#тестирование)*
- *[Лицензия](#лицензия)*
- *[Автор](#автор)*

## Технологии
- Python 3.12.7
- Poetry (управление зависимостями)
- Black (форматирование кода)
- Flake8 (стиль кода)
- Pytest (тестирование)
- Requests (HTTP-запросы)
- python-dotenv (переменные окружения)
- Pandas & openpyxl

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
- Конвертация сумм транзакций в рубли через внешний API (Поддержка валют: USD, EUR)
- Настроено логирование операций и ошибок в файлы
- Загрузка транзакций из CSV, Excel и JSON файлов
- Поиск транзакций по описанию - фильтрация по ключевым словам
- Статистика по категориям - подсчет операций по типам транзакций
- CLI интерфейс - интерактивная работа через командную строку

## Поддерживаемые форматы данных

- **CSV**: с любым разделителем (запятая, точка с запятой, табуляция)
- **Excel**: .xlsx, .xls (любой лист по имени или индексу)
- **JSON**: стандартный формат транзакций

### Поддерживаемые структуры данных

- **JSON (вложенная)**: `{"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}`
- **CSV/XLSX (плоская)**: `{"amount": "100", "currency_code": "USD"}`

## Логирование

- Логи записываются в папку logs/ (в репозитории)
- У каждого модуля свой logger
- Формат: дата | модуль | имя функции* | уровень | сообщение  
  *Если в модуле более 1 функции сообщение лога также содержит имя функции
- Уровни: INFO (успехи), ERROR (ошибки), DEBUG(отладка)
- Пример: 2024.12.20 15:30:25: mask: ERROR: Номер карты должен быть > 0

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
<details>
<summary>Функции</summary>

```python
from src.mask import get_mask_card_number, get_mask_account
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.widget import mask_account_card, get_date
from src.utils import load_transactions
from src.external_api import convert_transaction_to_rub
from src.data_loader import read_csv_transactions, read_excel_transactions
from src.analysis import filter_by_description, get_category_counts

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

# Загрузка из CSV
transactions_csv = read_csv_transactions("data/ops.csv", delimiter=";")
# Возвращает list[dict], например: [{'id': 1, 'date': '2024-01-01', ...}, ...]

# Загрузка из Excel  
transactions_excel = read_excel_transactions("data/ops.xlsx", sheet_name="Транзакции")
# Возвращает list[dict] [{'id': 2, 'date': '2025-01-01', ...}, ...]

# Поиск по описанию
transactions = [{"description": "Перевод организации"}, {"description": "Покупка в магазине"}]
filter_by_description(transactions, "Перевод")
# [{'description': 'Перевод организации'}]

# Статистика по категориям
transactions = [
    {"description": "Перевод"},
    {"description": "Перевод"},
    {"description": "Покупка"}
]
get_category_counts(transactions, ["Перевод", "Покупка"])
# {'Перевод': 2, 'Покупка': 1}
```
</details>

<details>
<summary>Декораторы</summary>

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
</details>

<details>
<summary>CLI Приложение</summary>

```
python main.py

Программа предлагает:
Выбор формата данных (JSON/CSV/XLSX)
Фильтрацию по статусу транзакций
Сортировку по дате
Фильтрацию по валюте (RUB)
Поиск по ключевым словам в описании
Форматированный вывод результатов
```
</details>

## Запуск приложения
```
# Запуск CLI интерфейса
python main.py

# Или прямое использование функций Python (см. примеры выше)
```

###  **Пример сессии приложения**


```
Добро пожаловать в программу работы с банковскими транзакциями.

Выберите необходимый пункт меню:

1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
4. Выйти из программы.

Ввод: 2

Для обработки выбран CSV-файл.

Введите статус, для фильтрации.
Доступные статусы: EXECUTED, CANCELED, PENDING

Ввод: executed

Операции отфильтрованы по статусу 'EXECUTED'
Отсортировать операции по дате? (Да/Нет)

Ввод: да

По возрастанию или по убыванию?
Ввод: по возрастанию 

Выводить только рублевые транзакции? (Да/Нет)
Ввод: нет

Отфильтровать список транзакций по определенному слову в описании? (Да/Нет)

Ввод: да

Введите слово для поиска:

Ввод: Перевод

Распечатываю итоговый список транзакций...

Всего банковских операций в выборке: 555

01.01.2020 Перевод с карты на карту
American Express 2957 86** **** 4974 -> American Express 6990 78** **** 8331
Сумма: 12764.0 AZN

01.01.2020 Перевод организации
Visa 4485 54** **** 2146 -> Счет **7912
Сумма: 34119.0 CNY

04.01.2020 Перевод с карты на карту
American Express 2116 42** **** 1997 -> American Express 8012 98** **** 6841
Сумма: 20057.0 IDR

...
```


## Разработка
### Ключевые особенности реализации:
- Полное покрытие тестами (pytest)
- Поддержка multiple форматов данных (JSON, CSV, XLSX)
- Модульная архитектура с разделением ответственности
- Подробное логирование всех операций
- Обработка ошибок

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
