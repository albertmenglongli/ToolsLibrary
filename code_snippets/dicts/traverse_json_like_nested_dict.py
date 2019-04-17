"""
Usage:
    import json

    # data is a json-like dictionary
    data = {
        "key_root": {
            "key_holding_lst": [
                {
                    "nested_key1": "hello world"
                },
                {
                    "nested_key1": "Python is Cool"
                }
            ],
            "key_holding_dict": {
                "nested_key2": "Good Morning",
                "nested_key3": None,
            }
        }
    }
    new_data = traverse(data, lambda x: str.upper(x) if isinstance(x, str) else x)
    print(json.dumps(new_data, indent=2, ensure_ascii=False))

    # output: "hello world" -> "HELLO WORLD", "Python is Cool" -> "PYTHON IS COOL" ...
"""


def traverse(obj, leaf_fn=lambda x: x):
    def _traverse(_obj):
        if isinstance(_obj, dict):
            return {k: _traverse(v) for k, v in _obj.items()}
        elif isinstance(_obj, list):
            return [_traverse(elem) for elem in _obj]
        else:
            # no container, just values (str, int, float, null)
            return leaf_fn(_obj)

    return _traverse(obj)
