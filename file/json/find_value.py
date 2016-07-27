def _find_repr_values(json_repr, id):
    import json
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            try:
                results.append(a_dict[id.__repr__()])
            except KeyError:
                pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results


def find_first_found_value(json_repr, id):
    try:
        value_repr = _find_repr_values(json_repr, id)[0]
        return eval(value_repr)
    except:
        return None


def main():
    with open('json_repr_content.txt') as f:
        from functools import partial
        json_repr = ''.join(f.readlines()).strip()
        find_value = partial(find_first_found_value, json_repr)

        print find_value('uid')
        print find_value('cardId')

if __name__ == '__main__':
    main()
