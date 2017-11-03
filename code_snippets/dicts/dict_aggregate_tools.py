"""
Requirement like sum all the value of amount in the dict list:

my_lst = [{'amount': 1}, {'amount': 5}, {'amount': 10}]

"""


def aggregate_dicts_value_under_key(dic_lst, key, func, initial):
    from functools import reduce
    return reduce(lambda x, y: {key: func(x[key], y[key])}, dic_lst, {key: initial})[key]


if __name__ == '__main__':
    my_lst = [{'amount': 1}, {'amount': 5}, {'amount': 10}]

    import operator

    assert 16 == aggregate_dicts_value_under_key(my_lst, 'amount', operator.add, 0)

    assert 50 == aggregate_dicts_value_under_key(my_lst, 'amount', operator.mul, 1)

    assert 0 == aggregate_dicts_value_under_key([], 'amount', operator.add, 0)

    assert -16 == aggregate_dicts_value_under_key(my_lst, 'amount', lambda x, y: 0 - abs(x) - abs(y), 0)
