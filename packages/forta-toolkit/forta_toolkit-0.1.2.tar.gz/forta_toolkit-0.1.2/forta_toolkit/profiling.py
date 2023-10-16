"""Profile the performances of a bot."""

import cProfile
import functools
import logging
import pstats
import time

# TIMEIT ######################################################################

def timeit(func: callable) -> callable:
    """Decorate a function to automatically log its execution time."""
    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        __start = time.perf_counter()
        __result = func(*args, **kwargs)
        __delta = 1000. * (time.perf_counter() - __start)
        logging.debug(f'{func.__name__} took {__delta:.9f} ms')
        return __result
    return __wrapper

# STATS #######################################################################

def profile(func: callable) -> callable:
    """Decorate a function to automatically collect performance statistics on its execution."""
    @functools.wraps(func)
    def __wrapper(*args, **kwargs):
        __profiler = cProfile.Profile()
        __profiler.enable()
        __result = func(*args, **kwargs)
        __profiler.disable()
        __profiler.dump_stats(f'{func.__name__}')
        return __result
    return __wrapper

# TESTS #######################################################################

@profile
def test_performances(func: callable, data: tuple) -> None:
    """Profile a function with the provided data."""
    (func(__d) for __d in data)

def display_performances(logpath: str) -> str:
    """Breakdown the performances of the full chain of execution in a table."""
    _p = pstats.Stats(logpath)
    return _p.strip_dirs().sort_stats('cumulative').print_stats()
