def memo(func):
    import json
    import hashlib
    try:
        # for python3.x
        from inspect import signature
    except ImportError:
        # for python2.x, need external dependency
        from funcsigs import signature

    # the cache could be any caches
    # for instance: django's LocMemCache cache or redis cache
    cache = {}

    def wrap(*args, **kwargs):
        sig = signature(func)
        params_ordered_dict = sig.bind(*args, **kwargs).arguments
        json_str = json.dumps(dict(params_ordered_dict), sort_keys=True)
        cache_key = hashlib.sha256(json_str.encode('utf-8')).hexdigest()
        if cache_key not in cache:
            cache[cache_key] = func(*args, **kwargs)
        return cache[cache_key]

    return wrap


@memo
def foo(a, b):
    return a + b


if __name__ == '__main__':
    print(foo(3, 5))
    print(foo(3, b=5))
    print(foo(a=3, b=5))
