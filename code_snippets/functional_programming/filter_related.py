def demo_filter_under_multi_criteria():
    """
    filter under multi criteria
    :return: 
    """
    from functools import reduce
    filters = [
        lambda e: e % 5 != 0,
        lambda e: e % 3 != 0,
    ]

    iterable = range(1, 20)

    # [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]
    result = list(reduce(lambda s, f: filter(f, s), filters, iterable))
    print(result)


demo_filter_under_multi_criteria()
