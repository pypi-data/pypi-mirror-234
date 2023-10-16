import functools
import time
from typing import Any, Callable


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that times the execution of a function.

    Args:
        func: The function to be timed.

    Returns:
        A wrapped function that times the execution of the original function.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:0.4f} seconds for {func.__name__}")
        return value

    return wrapper_timer
