from contextlib import contextmanager
from time import perf_counter


@contextmanager
def catchtime(message, enabled=True) -> float:
    start = perf_counter()
    yield
    if enabled:
        print(f"{perf_counter() - start:.3f} seconds to {message}")
