import logging
import re
from collections import Counter

logger = logging.getLogger("analysis")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/analysis.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def filter_by_description(operations: list[dict], search_string: str) -> list[dict]:
    """Возвращает операции, содержащие search_string в описании."""

    if not operations:
        logger.warning(f"Получен пустой список операций {operations}")
        return []

    logger.info(f"Поиск операций по {search_string} в описании.")
    pattern = re.escape(search_string)

    result = []

    for operation in operations:
        description = operation.get("description")
        if isinstance(description, str) and re.search(pattern, description, flags=re.I):
            result.append(operation)

    logger.info(f"Найдено {len(result)} совпадений")

    return result


def get_category_counts(operations: list[dict], categories: list[str]) -> dict[str, int]:
    """Подсчитывает операции по заданным категориям.
    Категория считается совпавшей только при точном равенстве описания."""

    logger.info(f"Подсчет операций по категориям: {categories}")
    counter: Counter = Counter()

    for operation in operations:
        description = operation.get("description")
        if isinstance(description, str):
            if description in categories:
                counter[description] += 1

    result = dict(counter)
    logger.info(f"Подсчет завершен, результат: {result}")

    return result
