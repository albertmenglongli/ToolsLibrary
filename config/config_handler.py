import copy
import json


class ParameterBasedSingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        parameter_hash = hash(json.dumps(args) + json.dumps(kwargs))
        instance_key = cls.__name__ + str(parameter_hash)
        if instance_key not in cls._instances:
            cls._instances[instance_key] = super(
                ParameterBasedSingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[instance_key]


class ConfigHandler(dict):

    __metaclass__ = ParameterBasedSingletonMetaClass

    def __init__(self, dic):
        self.default = dic['default']
        my_dic = {}
        for first_level_key in dic.keys():
            if first_level_key == 'default':
                continue
            my_dic.update({first_level_key: copy.deepcopy(self.default)})
            for inner_key, inner_value in dic[first_level_key].items():
                my_dic[first_level_key][inner_key] = inner_value

        super(ConfigHandler, self).__init__(my_dic)

    def __getitem__(self, key):
        try:
            value = super(ConfigHandler, self).__getitem__(key)
        except KeyError:
            # if key not found, we'll just return a copy of default;
            value = copy.deepcopy(self.default)
        return value


if __name__ == '__main__':
    from config import Countries, People

    countries = ConfigHandler(Countries)
    print countries['China']['language']
    # Chinese
    print countries['USA']['language']
    # American English
    print countries['GB']['language']
    # Common English

    people = ConfigHandler(People)
    print people['Bob']['full_name']
    print people['menglong']['full_name']

    # Using the same instance: countries
    print ConfigHandler(Countries)['China']['language']
    # Chinese

    assert (id(ConfigHandler(Countries)) == id(countries))
    assert (id(ConfigHandler(Countries)) != id(people))
