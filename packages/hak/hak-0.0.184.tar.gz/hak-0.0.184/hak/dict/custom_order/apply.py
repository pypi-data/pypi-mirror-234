from copy import deepcopy
from hak.pxyf import f as pxyf

# apply_custom_order
def f(x):
  order = deepcopy(x['order'])
  names = [n for n in x['names'] if n not in order]
  return order + names

t = lambda: pxyf(
  {'order': list('cba'), 'names': list('abcdef')},
  ['c', 'b', 'a', 'd', 'e', 'f'],
  f
)
