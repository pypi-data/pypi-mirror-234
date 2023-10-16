from datetime import timedelta
import time

_start_time = None


def tic():
    """
    Record the current time for later use with the `tac` function.
    """
    global _start_time
    _start_time = time.monotonic()


def tac():
    """
    Calculate the time elapsed since `tic` was called and print the result in hours, minutes, and seconds.
    """
    if _start_time is None:
        raise ValueError("The `tic` function must be called before the `tac` function.")

    elapsed_time = time.monotonic() - _start_time
    elapsed_time_str = str(timedelta(seconds=elapsed_time))

    print(f"Time passed: {elapsed_time_str}")
