from abc import ABCMeta, abstractmethod
from typing import Any
from design_patterns.commands.toolbox import AutoLoadField, Blackboard, UNSIGNED


class BaseCommand(metaclass=ABCMeta):
    """
    The Command interface declares a method for executing a command.
    """

    def __init__(self):
        self.auto_load_fields = []
        for att_name in self.__dict__:
            att_val = getattr(self, att_name, None)
            if att_val is AutoLoadField or isinstance(att_val, AutoLoadField):
                if not att_name.startswith('_'):
                    self.auto_load_fields.append(att_name)
        self.blackboard = Blackboard()

    def auto_load(self):
        for att_name in self.auto_load_fields:
            att_val = self.blackboard.get(att_name, UNSIGNED)
            if att_val is UNSIGNED:
                raise ValueError(f'{att_name} value is not provided')
            setattr(self, att_name, att_val)

    def set_blackboard(self, blackboard: Blackboard):
        self.blackboard = blackboard
        return self

    @abstractmethod
    def execute(self) -> Any:
        self.auto_load()


class EmptyCommand(BaseCommand):
    """
    Used as placeholder, do nothing
    """

    def execute(self) -> Any:
        pass


class UpdateBlackboardCommand(BaseCommand):
    """
    Update info on blackboard
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(UpdateBlackboardCommand, self).__init__()

    def execute(self) -> Any:
        self.blackboard.update(self.kwargs)
