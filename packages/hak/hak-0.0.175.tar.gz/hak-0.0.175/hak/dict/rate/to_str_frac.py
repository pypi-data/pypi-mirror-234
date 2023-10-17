from hak.dict.rate.make import f as rate
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  if x['denominator'] == 0: return f"undefined"
  if x['numerator'] == 0: return f""
  if x['denominator'] == 1: return f"{x['numerator']}"
  return f"{x['numerator']}/{x['denominator']}"

def t():
  if not pxyf(rate(710, 113, {'a': 1}), '710/113', f): return pf('!t_a')
  if not pxyf(rate(2, 1, {'a': 1}), '2', f): return pf('!t_b')
  if not pxyf(rate(0, 1, {'a': 1}), '', f): return pf('!t_c')
  if not pxyf(rate(1, 0, {'a': 1}), 'undefined', f): return pf('!t_d')
  return 1
