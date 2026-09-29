from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(
    filename: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логирует выполнение функции."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"

            except Exception as error:
                log_message = f"{func.__name__} error: {error}. " f"Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message + "\n")
                else:
                    print(log_message)

                raise

            if filename:
                with open(filename, "a") as file:
                    file.write(log_message + "\n")
            else:
                print(log_message)

            return result

        return wrapper

    return decorator
