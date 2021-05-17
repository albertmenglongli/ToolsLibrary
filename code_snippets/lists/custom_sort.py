def sort_with_custom_orders(values, key=lambda x: x, prefix_orders=None, suffix_orders=None):
    from collections import defaultdict

    if not prefix_orders:
        prefix_orders = []
    prefix_orders = list(prefix_orders)
    prefix_orders_set = set(prefix_orders)

    if len(prefix_orders) != len(prefix_orders_set):
        raise ValueError('prefix_order contains duplicated values')

    if not suffix_orders:
        suffix_orders = []
    suffix_orders = list(suffix_orders)
    suffix_orders_set = set(suffix_orders)

    if len(suffix_orders) != len(suffix_orders_set):
        raise ValueError('suffix_orders contains duplicated values')

    if prefix_orders_set.intersection(suffix_orders_set):
        # have some values in both prefix and suffix
        raise ValueError('prefix and suffix contains same value')

    order_map = defaultdict(lambda: 1)
    for idx, item in enumerate(prefix_orders):
        order_map[item] = idx - len(prefix_orders)

    for idx, item in enumerate(suffix_orders, start=2):
        order_map[item] = idx

    sorted_values = sorted(values, key=lambda x: (x not in prefix_orders_set, order_map[x], key(x)))

    return sorted_values


if __name__ == '__main__':
    values = ['h2', 'h1', 't2', 't1', 'B', 'a', 'Y', 'x']

    assert sorted(values) == ['B', 'Y', 'a', 'h1', 'h2', 't1', 't2', 'x']
    assert sorted(values, key=str.lower) == ['a', 'B', 'h1', 'h2', 't1', 't2', 'x', 'Y']

    # h (h1, h2) stands for headers, t (t1, t2) stands for tails
    sorted_values = sort_with_custom_orders(values, key=str.lower,
                                            prefix_orders=['h1', 'h2', 'h3'],
                                            suffix_orders=['t1', 't2', 't3'])

    assert sorted_values == ['h1', 'h2', 'a', 'B', 'x', 'Y', 't1', 't2']
