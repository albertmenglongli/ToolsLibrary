from typing import Optional, Union, List
from design_patterns.commands.base_command import BaseCommand
from design_patterns.commands.toolbox import Blackboard


class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
    to the command.
    """

    def __init__(self, blackboard: Optional[Union[dict, Blackboard]] = None,
                 commands: Optional[List[BaseCommand]] = None):

        blackboard_instance = self._parse_blackboard(blackboard)
        self.blackboard = blackboard_instance

        if commands is None:
            commands = []
        self._commands = commands
        self._bind_blackboard()

        self._outputs = []
        self._run_flg = False

    def _bind_blackboard(self):
        for cmd in self._commands:
            cmd.blackboard = self.blackboard

    @classmethod
    def _parse_blackboard(cls, blackboard):
        if not blackboard:
            blackboard_instance = Blackboard()
        elif isinstance(blackboard, Blackboard):
            blackboard_instance = blackboard
        elif isinstance(blackboard, dict):
            blackboard_instance = Blackboard()
            blackboard_instance.update(blackboard)
        else:
            raise ValueError('Invalid blackboard parameter')
        return blackboard_instance

    def set_blackboard(self, blackboard: Optional[Union[dict, Blackboard]] = None):
        blackboard_instance = self._parse_blackboard(blackboard)
        self.blackboard = blackboard_instance
        self._bind_blackboard()
        return self

    def set_commands(self, commands: Optional[List[BaseCommand]] = None):
        self._commands = commands
        self._bind_blackboard()
        return self

    @classmethod
    def build_invoker(cls, commands, blackboard=None):
        invoker = Invoker().set_blackboard(blackboard).set_commands(commands)
        return invoker

    @property
    def output(self):
        outputs = filter(lambda o: isinstance(o, str), self._outputs)
        return ''.join(outputs)

    def invoke(self) -> None:
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """
        if self._run_flg:
            raise RuntimeError('Invoke can only be invoked one time, already invoked')

        for cmd in self._commands:
            self._run_flg = True
            if isinstance(cmd, BaseCommand):
                output = cmd.execute()
                self._outputs.append(output)
