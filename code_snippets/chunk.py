'''
Usages:
Some time the lst is too big, so we just cut it into pieces
for sub_lst in chunks(lst, 500):
  pass
'''

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in xrange(0, len(lst), n):
        yield lst[i:i + n]
