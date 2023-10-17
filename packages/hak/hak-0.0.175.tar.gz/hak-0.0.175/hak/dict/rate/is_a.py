from hak.pf import f as pf
from hak.dict.rate.make import f as mk_rate
from hak.pxyf import f as pxyf

def f(x):
  if not isinstance(x, dict): return 0
  if not 'numerator' in x: return 0
  if not 'denominator' in x: return 0
  if not 'unit' in x: return 0
  return 1

t_true_units = lambda: pxyf(mk_rate(1, 2, {'m': 2, 's': -1}), 1, f)

def t():
  if not pxyf(mk_rate(1, 2, {}), 1, f): return pf('!t_true()')
  if not t_true_units(): return pf('!t_true_units()')
  if not pxyf('abc', 0, f): return pf('!t_false()')
  return 1
