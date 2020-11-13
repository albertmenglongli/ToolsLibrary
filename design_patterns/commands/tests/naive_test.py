from design_patterns.commands.invoker import Invoker
from design_patterns.commands.base_command import BaseCommand


class PrepareMaterialCommand(BaseCommand):
    def __init__(self, material):
        self.material = material
        super(PrepareMaterialCommand, self).__init__()

    def execute(self):
        print(f"{__class__.__name__}: Material '{self.material}' Prepared!")


if __name__ == '__main__':
    commands = [PrepareMaterialCommand('bread'), PrepareMaterialCommand('meat')]
    invoker = Invoker.build_invoker(commands=commands)
    invoker.invoke()
    """
    # PrepareMaterialCommand: Material 'bread' Prepared!
    # PrepareMaterialCommand: Material 'meat' Prepared!
    """
