from design_patterns.commands.invoker import Invoker
from design_patterns.commands.base_command import BaseCommand, UpdateBlackboardCommand
from design_patterns.commands.toolbox import auto_load_field


class PrepareMaterialCommand(BaseCommand):
    def __init__(self, material):
        self.material = material
        super(PrepareMaterialCommand, self).__init__()

    def execute(self):
        # update info in blackboard
        material_list = self.blackboard.get('material_list', [])
        material_list.append(self.material)
        self.blackboard.update({'material_list': material_list})

        # do own stuff
        output = f"{__class__.__name__}: Material '{self.material}' Prepared!\n"
        return output


class HeatCommand(BaseCommand):
    def __init__(self, material_list=auto_load_field):
        self.material_list = material_list
        super(HeatCommand, self).__init__()

    def execute(self):
        # auto load field from blackboard for those attributes with value -- `auto_load_filed`
        self.auto_load()

        # self.material_list load value from blackboard
        material_list = self.material_list
        if not material_list:
            output = f'{__class__.__name__}: Got nothing to heat!\n'
        else:
            output = f'{__class__.__name__}: Got {len(material_list)} materials: {material_list}, heat them!\n'

        return output


if __name__ == '__main__':
    # --------------------------------------------------------------------------------
    commands = [PrepareMaterialCommand('bread'), PrepareMaterialCommand('meat'), HeatCommand()]
    invoker = Invoker.build_invoker(commands=commands)  # commands in invoker share one blackboard
    invoker.invoke()
    print(invoker.output)
    """
    # PrepareMaterialCommand: Material 'bread' Prepared!
    # PrepareMaterialCommand: Material 'meat' Prepared!
    # HeatCommand: Got 2 materials: ['bread', 'meat'], heat them!
    """

    # --------------------------------------------------------------------------------
    commands = [PrepareMaterialCommand('bread'), PrepareMaterialCommand('meat'), HeatCommand()]
    blackboard = {'material_list': ['egg']}
    invoker = Invoker.build_invoker(commands=commands, blackboard=blackboard)
    invoker.invoke()
    print(invoker.output)
    """
    # PrepareMaterialCommand: Material 'bread' Prepared!
    # PrepareMaterialCommand: Material 'meat' Prepared!
    # HeatCommand: Got 3 materials: ['egg', 'bread', 'meat'], heat them!
    """

    # --------------------------------------------------------------------------------
    commands = [PrepareMaterialCommand('bread'), PrepareMaterialCommand('meat'),
                UpdateBlackboardCommand(material_list=[]),  # all materials removed accidentally, Oops!
                HeatCommand()]

    invoker = Invoker.build_invoker(commands=commands, blackboard=blackboard)
    invoker.invoke()
    print(invoker.output)
    """
    # PrepareMaterialCommand: Material 'bread' Prepared!
    # PrepareMaterialCommand: Material 'meat' Prepared!
    # HeatCommand: Got nothing to heat!
    """

    # --------------------------------------------------------------------------------
