from hak.bools.count_true import f as count_true
from hak.pxyf import f as pxyf

# positives
f = lambda x: count_true([_ > 0 for _ in [x[k] for k in x]]) if x else 0

t = lambda: pxyf({'a': 1, 'b': 0, 'c': -1, 'd': 2, 'e': -2, 'f': -3}, 2, f)
