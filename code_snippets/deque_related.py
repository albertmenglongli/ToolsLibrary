from collections import deque

def deque_split(d, nth):
    import itertools
    return deque(itertools.islice(d, nth)), deque(itertools.islice(d, nth, len(d)))
    
def delete_nth(d, nth):
    d.rotate(-nth)
    d.popleft()
    d.rotate(nth)
