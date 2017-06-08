def flatten(nested_dict, result=None, prefix=''):
    from collections import OrderedDict
    if result is None:
        result = dict()
    for k, v in nested_dict.items():
        new_k = '__'.join((prefix, k)) if prefix else k
        if not (isinstance(v, dict) or isinstance(v, OrderedDict)):
            result.update({new_k: v})
        else:
            flatten(v, result, new_k)
    return result


def rebuild(flatten_dict, result=None):
    from collections import defaultdict
    import json

    def tree():
        return defaultdict(tree)

    def rec(keys_iter, value):
        _r = tree()
        try:
            _k = next(keys_iter)
            _r[_k] = rec(keys_iter, value)
            return _r
        except StopIteration:
            return value

    if result is None:
        result = dict()

    for k, v in flatten_dict.items():
        keys_nested_iter = iter(k.split('__'))
        cur_level_dict = result
        while True:
            try:
                k = next(keys_nested_iter)
                if k in cur_level_dict:
                    cur_level_dict = cur_level_dict[k]
                else:
                    cur_level_dict[k] = json.loads(json.dumps(rec(keys_nested_iter, v)))
            except StopIteration:
                break

    return result


if __name__ == "__main__":
    my_dict = {'a': 'A',
               'b':
                   {
                       'd': [4, 44, 444],
                       'c': 'BC'
                   }
               }

    my_flatten_dict = flatten(my_dict)
    assert my_flatten_dict == {'a': 'A', 'b__c': 'BC', 'b__d': [4, 44, 444]}

    my_nested_dict = rebuild(my_flatten_dict)
    assert my_nested_dict == {'a': 'A', 'b': {'c': 'BC', 'd': [4, 44, 444]}}
