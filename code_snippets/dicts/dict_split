# coding: utf-8

import funcy
import itertools
from pprint import PrettyPrinter

my_dict = {
    'a': {
        'b': ['b1', 'b2', 'b3'],
        'c': 'C',
    },
    'd': 'D',
    'e': ['e1', 'e2', 'e3', 'e4', 'e5']
}


def split_dict_doppelgangers_by_keys(input_dict, keys):
    values = funcy.get_in(input_dict, keys)
    assert isinstance(values, list)

    paris = zip(itertools.repeat(input_dict), values)
    doppelgangers = list(map(lambda pair: funcy.set_in(pair[0], keys, pair[1]), paris))
    return doppelgangers


pp = PrettyPrinter()
pp.pprint(split_dict_doppelgangers_by_keys(my_dict, ['a', 'b']))
pp.pprint(split_dict_doppelgangers_by_keys(my_dict, ['e']))

# [{'a': {'b': 'b1', 'c': 'C'}, 'd': 'D', 'e': ['e1', 'e2', 'e3', 'e4', 'e5']},
#  {'a': {'b': 'b2', 'c': 'C'}, 'd': 'D', 'e': ['e1', 'e2', 'e3', 'e4', 'e5']},
#  {'a': {'b': 'b3', 'c': 'C'}, 'd': 'D', 'e': ['e1', 'e2', 'e3', 'e4', 'e5']}]
# [{'a': {'b': ['b1', 'b2', 'b3'], 'c': 'C'}, 'd': 'D', 'e': 'e1'},
#  {'a': {'b': ['b1', 'b2', 'b3'], 'c': 'C'}, 'd': 'D', 'e': 'e2'},
#  {'a': {'b': ['b1', 'b2', 'b3'], 'c': 'C'}, 'd': 'D', 'e': 'e3'},
#  {'a': {'b': ['b1', 'b2', 'b3'], 'c': 'C'}, 'd': 'D', 'e': 'e4'},
#  {'a': {'b': ['b1', 'b2', 'b3'], 'c': 'C'}, 'd': 'D', 'e': 'e5'}]
