from contextlib import contextmanager
from timeit import default_timer

__all__ = ["elapsed_timer"]


@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start  # type: ignore
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end - start
