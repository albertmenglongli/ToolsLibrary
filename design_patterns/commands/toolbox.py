from collections import ChainMap
from typing import Optional


class AutoLoadField:
    pass


class Empty:
    pass


class Blackboard:
    def __init__(self, data: Optional[dict] = None):
        if data is None:
            data = {}
        self.core = ChainMap(data)

    def to_dict(self):
        return dict(self.core)

    def __getitem__(self, item):
        return self.core[item]

    def get(self, item, default=None):
        return self.core.get(item, default)

    def update(self, new_dct: dict):
        self.core = self.core.new_child(new_dct)

    def __str__(self):
        return str(self.core)

    def __repr__(self):
        return str(self)


UNSIGNED = Empty()
auto_load_field = AutoLoadField()
