import logging
import re

logger = logging.getLogger("analysis")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/analysis.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def filter_by_description(operations: list[dict], search_string: str) -> list[dict]:
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
