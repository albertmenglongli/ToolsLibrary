from contextlib import contextmanager
import random


@contextmanager
def context_random(seed):
    old_state = random.getstate()
    try:
        random.seed(seed)
        yield random
    finally:
        random.setstate(old_state)


try:
    with context_random('111') as random:
        print(random.random())
        print(random.choice(range(1, 100)))
        raise Exception()
except:
    pass

print(random.random())
print(random.choice(range(1, 100)))
