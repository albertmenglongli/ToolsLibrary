from contextlib import contextmanager


@contextmanager
def random_context(random_module, seed):
    assert random_module in ('random', 'numpy.random')

    if random_module == 'random':
        import random as _random
        get_state_method_str = 'getstate'
        set_state_method_str = 'setstate'
    elif random_module == 'numpy.random':
        from numpy import random as _random
        get_state_method_str = 'get_state'
        set_state_method_str = 'set_state'
    else:
        raise Exception('Not supported random module {random_module}'.format(random_module=random_module))

    old_state = getattr(_random, get_state_method_str)()
    try:
        _random.seed(seed)
        yield _random
    finally:
        getattr(_random, set_state_method_str)(old_state)


with random_context(random_module='random', seed=3) as r:
    print(r.random())
    print(r.choice(range(1, 100)))

with random_context(random_module='numpy.random', seed=3) as r:
    print(r.random())
    print(r.choice(range(1, 100)))

try:
    with random_context(random_module='random', seed=3) as r:
        print(r.random())
        print(r.choice(range(1, 100)))
        raise Exception()
except:
    pass
