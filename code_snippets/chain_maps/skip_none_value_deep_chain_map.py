from collections import ChainMap


class SkipNoneValueDeepChainMap(ChainMap):
    """
    Variant of ChainMap that by pass the None values in the inner scope,
    if the root contains None value for the key, the None will be returned.
    """

    def __getitem__(self, key):
        for mapping in self.maps:
            if key in mapping and (mapping[key] is not None or mapping == self.maps[-1]):
                return mapping[key]
        raise KeyError(key)


if __name__ == "__main__":
    my_globals = SkipNoneValueDeepChainMap({'name': 'anonymous', 'location': None})
    my_locals = my_globals.new_child({'name': None, 'location': None})

    # anonymous
    print(my_locals.get('name'))

    # None
    print(my_locals.get('location'))
