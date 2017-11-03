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
