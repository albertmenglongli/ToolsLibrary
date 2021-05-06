def convert_alias_dict_to_lookup_map(alias_dict):
    from itertools import zip_longest, chain, dropwhile, tee
    import types
    from collections import Counter
    alias_dict_copy = {}
    value_set = set()
    for key, value in alias_dict.items():
        # create copy of the alias_dict
        if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set):
            alias_dict_copy[key] = list(value)
        elif isinstance(value, types.GeneratorType):
            # deepcopy cannot handle generator types
            value, value_cp = tee(value, 2)
            alias_dict[key] = value
            alias_dict_copy[key] = list(value_cp)
        else:
            alias_dict_copy[key] = [value]

        # validate the alias dict
        value_counter = Counter(alias_dict_copy[key])
        for sub_key, cnt in dropwhile(lambda key_count: key_count[1] == 1, value_counter.items()):
            raise Exception('Duplicated alias for value {}'.format(sub_key))

        inter_set = set(alias_dict_copy[key]).intersection(value_set)
        if inter_set:
            raise Exception('Duplicated alias for value {}'.format(' '.join(inter_set)))
        value_set.update(set(alias_dict_copy[key]))

    # generate the map from alias dict transformed copy
    res = dict(chain.from_iterable(zip_longest(items[1], [items[0]], fillvalue=items[0])
                                   for items in alias_dict_copy.items()))
    return res


if __name__ == '__main__':
    # basic usage

    device_types = {
        'computer': ['mac', 'laptop', 'workstation', 'pc', 'server'],
        'phone': ['cellphone', 'telephone', 'iphone', 'mobile'],
    }
    lookup_map = convert_alias_dict_to_lookup_map(device_types)

    assert lookup_map == {
        'mac': 'computer',
        'laptop': 'computer',
        'workstation': 'computer',
        'pc': 'computer',
        'server': 'computer',
        'cellphone': 'phone',
        'telephone': 'phone',
        'iphone': 'phone',
        'mobile': 'phone',
    }
    assert lookup_map['mac'] == 'computer'
    assert lookup_map['workstation'] == 'computer'


    # support other data types like generator, set, tuple or raw string

    def phone_alias_generator():
        for alias in ['cellphone', 'telephone', 'iphone', 'mobile']:
            yield alias


    device_types = {
        'phone': phone_alias_generator(),  # generator
        'ipad': 'ipad pro',  # raw string
    }

    lookup_map = convert_alias_dict_to_lookup_map(device_types)
    assert lookup_map == {
        'cellphone': 'phone',
        'telephone': 'phone',
        'iphone': 'phone',
        'mobile': 'phone',
        'ipad pro': 'ipad'
    }

    # the original generator is untouched
    assert list(device_types['phone']) == ['cellphone', 'telephone', 'iphone', 'mobile']
    # the original generator is consumed
    assert list(device_types['phone']) == []
