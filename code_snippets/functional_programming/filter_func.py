def filter_multi(functions, iterable):
    from functools import reduce
    return list(reduce(lambda s, f: filter(f, s), functions, iterable))


if __name__ == "__main__":
    filters = [
        lambda e: e % 5 != 0,
        lambda e: e % 3 != 0,
    ]

    # [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]
    result = filter_multi(filters, range(1, 20))
    print(result)
