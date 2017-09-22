"""
Just for fun, to use yield, toooo much complicated than the filter_func's implementation.
"""

import functools
from copy import deepcopy


def coroutine(func):
    """
    this decorator will run the first next of the generator
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value


@coroutine
def gen_process_chain(handler, successor=None):
    try:
        while True:
            obj_list = (yield)
            try:
                if len(obj_list) > 0:
                    obj_list[:] = list(filter(handler, obj_list))[:]
            except Exception as e:
                import traceback
                print(traceback.format_exc())

            if successor:
                successor.send(obj_list)

    except GeneratorExit:
        if successor:
            successor.close()


def gen_pipeline(handlers):
    if not handlers:
        raise Exception("should at least have one handler")
    handlers.reverse()
    _pipeline_head_node = gen_process_chain(handlers[0])
    for handler in handlers[1:]:
        _pipeline_head_node = gen_process_chain(handler, _pipeline_head_node)
    return _pipeline_head_node


def filter_multi(funcs, iterable):
    lst = list(iterable)

    pipeline = gen_pipeline(funcs)
    try:
        result_list = deepcopy(lst)
        pipeline.send(result_list)
    except:
        pass
    else:
        return result_list
    finally:
        pipeline.close()


if __name__ == "__main__":
    filters = [
        lambda e: e % 5 != 0,
        lambda e: e % 3 != 0,
    ]

    # [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]
    result = filter_multi(filters, list(range(1, 20)))
    print(result)
