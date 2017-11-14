"""
Usages:
Some time the lst is too big, so we just cut it into pieces
for sub_lst in chunks(lst, 500):
  pass
"""


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# pip install PyFunctional
from functional import seq

# [[1, 2, 3], [4, 5, 6], [7, 8]]
for sub_list in seq([1, 2, 3, 4, 5, 6, 7, 8]).grouped(3):
    print(list(sub_list))
