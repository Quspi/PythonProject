import logging

logger = logging.getLogger("processing")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs/processing.log", "a", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def filter_by_state(items: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует операции по статусу. По умолчанию - выполненные."""
    logger.info(f"Фильтрация {len(items)} операций по {state}")
    result = []
    for item in items:
        if item.get("state") == state:
            result.append(item)
    logger.info(f"Результат фильтрации: {len(result)}/{len(items)} операций")
    return result


def sort_by_date(items: list[dict], sort_order: bool = True) -> list[dict]:
    """Сортирует операции по дате выполнения. По умолчанию - по убыванию."""
    logger.info(f"Сортировка {len(items)} операций по дате.")
    result = sorted(items, key=lambda x: x["date"], reverse=sort_order)
    logger.info(f"Успешно отсортировано {len(result)} операций")
    return result
