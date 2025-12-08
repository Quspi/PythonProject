from functools import wraps
from os import makedirs
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Логирует вызовы функции в файл или консоль, filename: если указан - пишет в файл, иначе - в консоль."""

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if filename:
                makedirs("logs", exist_ok=True)
                with open(f"logs/{filename}", "a", encoding="UTF-8") as f:
                    try:
                        result = function(*args, **kwargs)
                        f.write(f"{function.__name__} ok: {result}\n")
                        return result
                    except Exception as e:
                        f.write(f"{function.__name__} {type(e).__name__}: {str(e)}. Inputs: {args}, {kwargs}\n")

                        raise e
            else:
                try:
                    result = function(*args, **kwargs)
                    print(f"{function.__name__} ok: {result}\n")
                    return result
                except Exception as e:
                    print(f"{function.__name__} {type(e).__name__}: {str(e)}. Inputs: {args}, {kwargs}\n")

                    raise e

        return wrapper

    return decorator
