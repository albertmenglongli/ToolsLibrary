import sys


# Refs: https://stackoverflow.com/questions/57617744/context-manager-hackery
class SkipContextManager:
    class SkipWithBlock(Exception):
        pass

    def __init__(self, skip):
        self.skip = skip

    def __enter__(self):
        if self.skip:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)
            frame.f_trace = self.trace

    def trace(self, frame, event, arg):
        raise self.SkipWithBlock()

    def __exit__(self, type, value, traceback):
        if type is None:
            return  # No exception
        if issubclass(type, self.SkipWithBlock):
            return True  # Suppress special SkipWithBlock exception


if __name__ == '__main__':
    with SkipContextManager(skip=True):
        print('In the with block')  # Won't be called
    print('Out of the with block')
