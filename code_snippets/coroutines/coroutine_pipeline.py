import functools
from contextlib import contextmanager


def coroutine(function):
    """
    this decorator will run the first next of the generator
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


@coroutine
def gen_process_chain(handler, handle_method_name, successor=None):
    try:
        while True:
            obj_to_handle = (yield)
            try:
                getattr(handler, handle_method_name)(obj_to_handle)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
            if successor:
                successor.send(obj_to_handle)
    except GeneratorExit:
        if successor:
            successor.close()


def gen_pipeline(handlers, handle_method_name):
    if not handlers:
        raise Exception("should at least have one handler")
    handlers.reverse()
    _pipeline_head_node = gen_process_chain(handlers[0], handle_method_name)
    for handler in handlers[1:]:
        _pipeline_head_node = gen_process_chain(handler, handle_method_name, _pipeline_head_node)
    return _pipeline_head_node


@contextmanager
def responsibility_chain(*args):
    _pipeline = None
    try:
        _pipeline = gen_pipeline(*args)
        yield _pipeline
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise e
    finally:
        if _pipeline:
            _pipeline.close()


if __name__ == '__main__':
    class Handler(object):
        def __init__(self, msg_to_append):
            self.msg_to_append = msg_to_append

        def process(self, msg_lst):
            msg_lst.append(self.msg_to_append)


    handlers = [Handler(' nice weather, right?'), Handler(' Good to hear from you.')]
    with responsibility_chain(handlers, 'process') as chain:
        msg_lst = ['Got a letter']
        chain.send(msg_lst)
        print(msg_lst)  # ['Got a letter', ' nice weather, right?', ' Good to hear from you.']
        another_msg_lst = ['Reply']
        chain.send(another_msg_lst)  # ['Reply', ' nice weather, right?', ' Good to hear from you.']
        print(another_msg_lst)
