##Extra functions - batch creation, timer wrapper, etc.
import time
from functools import wraps
from .logging import logg

__all__ = ['timer', 'batch_generator', 'batch_create']

def timer(func=None, *, logger=...):
    """Decorator to time a function.

    Usage:
        @timer
        def f(...): ...

        @timer(logger=my_logger)
        def g(...): ...

    Notes:
        - Uses `logg.info(...)` (not `print`).
        - If `logger=None`, timing output is silenced.
    """

    if func is None:
        return lambda f: timer(f, logger=logger)

    @wraps(func)
    def wrapper(*args, **kwargs):
        before = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - before
        logg.info(f'function time : {elapsed} seconds', logger)
        return result

    return wrapper

def batch_generator(iterable, batch_size):
    """
    Generator to create batches of a given size from an iterable
    Input:
        iterable: iterable to be batched
        batch_size: size of the batches
    Output:
        batch: batch of the given size
    """
    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]

def batch_create(l, n,logger=None):
    """
    Create batches in a list of a size from a given list
    Input:
        l: list to be batched
        n: size of the batches
    Output:
        batch(list): batch of the given size
    """
    batch_create_list=[]
    for i in range(0, len(l), n):
        batch_create_list.append(l[i:i+n])
    logg.info("batches created : {}".format(len(batch_create_list)), logger)
    return batch_create_list