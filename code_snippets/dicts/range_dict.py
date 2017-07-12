class RangeDict:
    def __init__(self, my_dict):
        assert all(map(lambda x: isinstance(x, tuple) and len(x) == 2 and x[0] <= x[1], my_dict))

        def lte(bound):
            return lambda x: bound <= x

        def gt(bound):
            return lambda x: x < bound

        # generate the inner dict with tuple key like (lambda x: 0 <= x, lambda x: x < 100)
        self._my_dict = {(lte(k[0]), gt(k[1])): v for k, v in my_dict.items()}

    def __getitem__(self, number):
        from functools import reduce
        _my_dict = self._my_dict
        result = next((_my_dict[key] for key in _my_dict if list(reduce(lambda s, f: filter(f, s), key, [number]))),
                      KeyError)
        if result is KeyError:
            raise KeyError(number)
        return result

    def get(self, number, default=None):
        try:
            return self.__getitem__(number)
        except KeyError:
            return default


if __name__ == '__main__':
    range_dict = RangeDict({
        (0, 100): 'A',
        (100, 200): 'B',
        (200, 300): 'C',
    })

    # test normal case
    assert range_dict[70] == 'A'
    assert range_dict[170] == 'B'
    assert range_dict[270] == 'C'

    # test case when the number is float
    assert range_dict[70.5] == 'A'

    import contextlib


    @contextlib.contextmanager
    def raises(exception):
        try:
            yield
        except exception:
            assert True
        else:
            assert False


    with raises(KeyError):
        # raise a KeyError: 1000
        _ = range_dict[1000]

    # test case not in the range, with default value
    assert range_dict.get(1000, 'D') == 'D'
