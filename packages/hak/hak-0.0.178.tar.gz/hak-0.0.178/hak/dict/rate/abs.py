from hak.pf import f as pf
from hak.dict.rate.make import f as mk_rate
from hak.pxyf import f as pxyf

def f(x):
  if not isinstance(x, dict): raise ValueError(f'x: {x} is not a dict')
  return mk_rate(abs(x['numerator']), abs(x['denominator']), x['unit'])

t_a = lambda: pxyf(mk_rate(-1,  3, {'a': 1}), mk_rate( 1, 3, {'a': 1}), f)
t_b = lambda: pxyf(mk_rate(45, -7, {'b': 1}), mk_rate(45, 7, {'b': 1}), f)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
