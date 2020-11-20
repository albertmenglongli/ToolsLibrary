from functools import lru_cache, wraps
from typing import Any, Set, List, Union


def cache_unless(values: Union[List[Any], Set[Any]], typed=False):
    if not values:
        raise ValueError('Nothing to ignore! Plz use standard lru_cache!')

    if isinstance(values, (list, set)):
        values = set(values)
    else:
        raise ValueError('list or set values to be provided!')

    def decorator(user_function):
        lru_cached_user_function = lru_cache(maxsize=None, typed=typed)(user_function)

        @wraps(lru_cached_user_function)
        def wrapper(*args, **kwargs):
            result = lru_cached_user_function(*args, **kwargs)
            if result in values:
                lru_cached_user_function.cache_clear()
            return result

        # only expose the cache_clear function, no cache_info function
        # cause this function abuse the cache_info by call cache_clear when hit unless values
        # cache_info means nothing any more
        wrapper.cache_clear = lru_cached_user_function.cache_clear
        return wrapper

    return decorator


if __name__ == '__main__':

    def generate_token():
        yield None
        yield None
        yield ''
        yield 'token123'


    token_generator = generate_token()


    @cache_unless([None, ''])
    def get_token():
        """
        Get token from Internet or somewhere
        """
        token = next(token_generator)
        if token is None:
            print('fetch token failed')
        else:
            print(f"fetch token: {token}")
        return token


    assert get_token() is None  # fetch token failed
    assert get_token() is None  # fetch token failed
    assert get_token() == ''  # fetch token:
    assert get_token() == 'token123'  # fetch token: token123
    assert get_token() == 'token123'
    assert get_token() == 'token123'
