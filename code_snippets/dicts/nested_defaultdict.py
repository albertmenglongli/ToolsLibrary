"""
Usage:
    r = tree()

    r['a']['b']='bb'
    r['a']['c']['d']='dddd'

    import json
    print json.dumps(r)
    #{"a": {"c": {"d": "dddd"}, "b": "bb"}}

    print r['a']['b']
    #bb

    print r['a']['c']['d']
    #dddd
"""

from collections import defaultdict

tree = lambda: defaultdict(tree)


# converting nested defaultdict to normal nested dict
def ddict_to_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = ddict_to_dict(v)
    return dict(d)
