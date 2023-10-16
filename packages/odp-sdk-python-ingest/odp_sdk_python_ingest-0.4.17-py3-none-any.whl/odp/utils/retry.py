import logging
import random
import time
from functools import partial
from typing import Callable, ClassVar, Dict, List, Optional, Union

from decorator import decorator

logging_logger = logging.getLogger(__name__)


def __retry_internal(
    f: Callable,
    exceptions: ClassVar[Exception] = Exception,
    tries: int = -1,
    delay: Union[float, int] = 0,
    max_delay: Optional[Union[float, int]] = None,
    backoff: Union[float, int] = 1,
    jitter: Union[float, int] = 0,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    logger: Optional[logging.Logger] = logging_logger,
):
    """
    Executes a function and retries it if it failed.

    :param f: the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    _tries, _delay = tries, delay
    _cnt = 0
    while _tries:
        try:
            return f()
        except exceptions as e:
            _tries -= 1
            _cnt += 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning("%s, retrying in %s seconds...", e, _delay)

            if on_retry:
                t0 = time.time()
                on_retry(e, _cnt)
                dt = time.time() - t0

                if dt < _delay:
                    this_delay = _delay - dt
                else:
                    this_delay = 0
            else:
                this_delay = _delay

            time.sleep(this_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)


def retry(
    exceptions: ClassVar[Exception] = Exception,
    tries: int = -1,
    delay: Union[float, int] = 0,
    max_delay: Optional[Union[float, int]] = None,
    backoff: Union[float, int] = 1,
    jitter: Union[float, int] = 0,
    on_retry: Optional[Callable] = None,
    logger: Optional[logging.Logger] = logging_logger,
):
    """Returns a retry decorator.

    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: a retry decorator.
    """

    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return __retry_internal(
            partial(f, *args, **kwargs),
            exceptions,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            on_retry,
            logger,
        )

    return retry_decorator


def retry_call(
    f: Callable,
    fargs: Optional[List] = None,
    fkwargs: Optional[Dict] = None,
    exceptions: ClassVar[Exception] = Exception,
    tries: int = -1,
    delay: Union[float, int] = 0,
    max_delay: Optional[Union[float, int]] = None,
    backoff: Union[float, int] = 1,
    jitter: Union[float, int] = 0,
    on_retry: Optional[Callable] = None,
    logger: Optional[logging.Logger] = logging_logger,
):
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    args = fargs if fargs else list()
    kwargs = fkwargs if fkwargs else dict()
    return __retry_internal(
        partial(f, *args, **kwargs),
        exceptions,
        tries,
        delay,
        max_delay,
        backoff,
        jitter,
        on_retry,
        logger,
    )
