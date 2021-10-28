'''
 Asign id with value from userid, and if userid is None, try snsid, fpid, user_id in order.
'''
# Method 1

id = next((item for item in [data_dict.get('userid', None),
                             data_dict.get('snsid', None),
                             data_dict.get('fpid', None),
                             data_dict.get('user_id', None)] if item), None)

# Method 2
# Notice that this has Python recursive limitation

def until(terminate, iterator, default):
    if isinstance(iterator, list):
        iterator = iter(iterator)
    try:
        i = next(iterator)
        if terminate(i):
            return i
        return until(terminate, iterator, default)
    except StopIteration:
        return default


# candidates = [None, None, None, None]
candidates = [None, None, '25', None]
id = until(lambda x: x is not None, iter(candidates), '1')

# Method 3
# Introducing FP(Functional Programming)

from funcy import first, compact
candidates = [None, None, '25', None]
id = first(compact(candidates)) # 25

