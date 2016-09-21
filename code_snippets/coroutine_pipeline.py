'''
    # Usage: could be used as for-loop or responsibility-chain
    
    class Handler(object):
    
        def __init__(self, msg_to_append):
            self.msg_to_append = msg_to_append
    
        def process(self, msg_lst):
            msg_lst.append(self.msg_to_append)
    
    handlers = [Handler(' nice weather, right?'), Handler(' Good to here from you.')]
    pipeline = gen_pipeline(*handlers)
    msg_lst = ['Got a letter']
    pipeline.send(msg_lst)
    print msg_lst  # ['Got a letter', ' nice weather, right?', ' Good to here from you.']
    
    another_msg_lst = ['Reply']
    pipeline.send(another_msg_lst)  # ['Reply', ' nice weather, right?', ' Good to here from you.']
    print another_msg_lst
    pipeline.close()
'''

import functools

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
def gen_process_chain(handler, successor=None):
    try:
        while True:
            obj_to_handle = (yield)
            try:
                handler.process(obj_to_handle)
            except Exception as e:
                pass
            if successor:
                successor.send(obj_to_handle)
    except GeneratorExit:
        if successor:
            successor.close()


def gen_pipeline(*args):
    if not args:
        raise Exception("should at least have one handler")
    args_list = list(args)
    args_list.reverse()
    pipeline = gen_process_chain(args_list[0])
    for method in args_list[1:]:
        pipeline = gen_process_chain(method, pipeline)
    return pipeline
