from design_patterns.commands.invoker import Invoker
from design_patterns.commands.base_command import BaseCommand
from design_patterns.commands.toolbox import auto_load_field, AutoLoadField
from typing import Union


class AnimalConsumerCmd(BaseCommand):
    def __init__(self, animal, feed_on, menu: Union[dict, AutoLoadField] = auto_load_field):
        self.animal = animal
        self.feed_on = feed_on
        self.menu = menu
        super(AnimalConsumerCmd, self).__init__()

    def execute(self):
        # auto load field from blackboard for those attributes with value -- `auto_load_filed`
        self.auto_load()

        if self.menu.get(self.feed_on, 0) == 0:
            print(f'{self.animal}: No {self.feed_on} on menu, oops!')
        else:
            self.menu[self.feed_on] = self.menu[self.feed_on] - 1
            # update blackboard, that one food is consumed
            self.blackboard.update({'menu': self.menu})
            print(f'{self.animal}: eat one {self.feed_on}, yummy!')


if __name__ == '__main__':
    # --------------------------------------------------------------------------------
    blackboard = {
        'menu': {
            'banana': 2,
            'fish': 1,
        }
    }
    commands = [AnimalConsumerCmd(animal='Monkey1', feed_on='banana'),
                AnimalConsumerCmd(animal='Cat1', feed_on='fish'),
                AnimalConsumerCmd(animal='Cat2', feed_on='fish')]
    invoker = Invoker.build_invoker(commands=commands, blackboard=blackboard)
    invoker.invoke()
    """
    # Monkey1: eat one banana, yummy!
    # Cat1: eat one fish, yummy!
    # Cat2: No fish on menu, oops!
    """

    # --------------------------------------------------------------------------------
    # same as above, but this time, not pass blackboard explicit,
    # pass a menu to the first monkey
    menu = {
        'banana': 2,
        'fish': 1,
    }
    commands = [AnimalConsumerCmd(animal='Monkey1', feed_on='banana', menu=menu),
                AnimalConsumerCmd(animal='Cat1', feed_on='fish'),
                AnimalConsumerCmd(animal='Cat2', feed_on='fish')]
    invoker = Invoker.build_invoker(commands=commands)
    invoker.invoke()
    """
    # Monkey1: eat one banana, yummy!
    # Cat1: eat one fish, yummy!
    # Cat2: No fish on menu, oops!
    """

    # --------------------------------------------------------------------------------
