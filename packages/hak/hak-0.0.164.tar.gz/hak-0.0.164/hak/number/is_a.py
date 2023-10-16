from numbers import Number

from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: isinstance(x, Number)

def t():
  if not pxyf(None, 0, f): return pf('!t_false_None')
  if not pxyf('0', 0, f): return pf('!t_false_str')
  if not pxyf(0.1j + 5, 1, f): return pf('!t_true_complex')
  if not pxyf(0.1, 1, f): return pf('!t_true_float')
  if not pxyf(0, 1, f): return pf('!t_true_zero')
  return 1
