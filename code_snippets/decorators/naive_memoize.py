# This was used for algorithm when recurse happened for Python 2.7

# After Python 3.2+ we can use @functools.lru_cache(maxsize=128, typed=False):
#   If maxsize is set to None, the LRU feature is disabled and the cache can grow without bound.
#       The LRU feature performs best when maxsize is a power-of-two.
#   If typed is set to true, function arguments of different types will be cached separately.
#       For example, f(3) and f(3.0) will be treated as distinct calls with distinct results.


def memo(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap
