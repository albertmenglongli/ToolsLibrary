import copy
import json

DEFAULT_KEY = 'default'


class ParameterBasedSingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args):
        # using json strings, because some types are not hashable (list, for
        # instance)
        parameter_hash = hash(json.dumps(args))
        instance_key = cls.__name__ + str(parameter_hash)
        if instance_key not in cls._instances:
            cls._instances[instance_key] = super(
                ParameterBasedSingletonMetaClass, cls).__call__(*args)
        return cls._instances[instance_key]


class OneLayerConfigHandler(dict):
    """
    Config handler only supports default config for one layer
    """
    __metaclass__ = ParameterBasedSingletonMetaClass

    def __init__(self, dic):

        self.default_value = copy.deepcopy(dic[DEFAULT_KEY])
        my_dic = {}
        for default_layer_key in dic.keys():
            if default_layer_key == DEFAULT_KEY:
                continue
            my_dic.update(
                {
                    default_layer_key: copy.deepcopy(self.default_value)
                })
            for inner_key, inner_value in dic[default_layer_key].items():
                my_dic[default_layer_key][inner_key] = inner_value

        super(OneLayerConfigHandler, self).__init__(my_dic)

    def __getitem__(self, key):
        try:
            value = super(OneLayerConfigHandler, self).__getitem__(key)
        except KeyError:
            # if key not found, we'll just return a copy of default value;
            value = copy.deepcopy(self.default_value)
        return value


class NestedConfigHandler(dict):
    """
    Config handler supports default config with nested layers
    """

    def __init__(self, dic):
        # Todo: for now, list is not supported in the nested config, only dict
        # nested in dict
        dic_copy = copy.deepcopy(dic)
        self.default_value = dic_copy.get(DEFAULT_KEY, None)
        if DEFAULT_KEY in dic_copy:
            del dic_copy[DEFAULT_KEY]
        my_dic = {}
        for default_sibling_key in dic_copy.keys():
            my_dic.update(
                {default_sibling_key: copy.deepcopy(self.default_value)})
            for inner_key, inner_value in dic[default_sibling_key].items():
                if isinstance(inner_value, dict) and inner_key in self.default_value:
                    my_dic[default_sibling_key].update(NestedConfigHandler(
                        {
                            DEFAULT_KEY: self.default_value[inner_key],
                            inner_key: inner_value,
                        }))
                else:
                    my_dic[default_sibling_key][inner_key] = inner_value

        super(NestedConfigHandler, self).__init__(my_dic)


if __name__ == '__main__':
    """
    Please compare with the configs in config.py to understand the testing codes below
    """
    from config import Countries, People

    COUNTRIES_CONFIG = OneLayerConfigHandler(Countries)
    print(COUNTRIES_CONFIG['China']['language'])
    # >> Chinese
    print(COUNTRIES_CONFIG['USA']['language'])
    # >> American English
    print(COUNTRIES_CONFIG['GB'])
    # >> {'location': 'on Earth in Galaxy', 'language': 'Common English'}
    print(COUNTRIES_CONFIG['GB']['language'])
    # >> Common English

    SIMPLE_PEOPLE_CONFIG = OneLayerConfigHandler(People)
    print(SIMPLE_PEOPLE_CONFIG['Bob']['full_name'])
    # >> Mr. Unknown
    print(SIMPLE_PEOPLE_CONFIG['menglong']['full_name'])
    # >> Li, Menglong

    """
    In the simple config handler, we cannot handle the nested cases with default
    """
    # print(SIMPLE_PEOPLE_CONFIG['menglong']['language']['Japanese']['level']
    # >> KeyError: 'Japanese'

    # testing the Singleton using hash
    assert (id(OneLayerConfigHandler(Countries)) != id(SIMPLE_PEOPLE_CONFIG))

    # using nested config handler, we can handle
    # nested cases, with default value
    NESTED_PEOPLE_CONFIG = NestedConfigHandler(People)
    print(NESTED_PEOPLE_CONFIG['menglong'])
    # >> {
    #       'key_not_in_default': {'des': 'which is not recommended'},
    #       'full_name': 'Li, Menglong',
    #       'language': {'Japanese': {'level': 0}, 'Chinese': 'Mother Tougue', 'English': 'Soso'},
    #       'skin': 'yellow',
    #       'gender': 'male'
    #    }
    print(NESTED_PEOPLE_CONFIG['menglong']['language']['Japanese']['level'])
    # >> 0
