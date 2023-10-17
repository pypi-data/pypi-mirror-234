from hak.dict.rate.div_rate_by_rate import f as div_rate_by_rate
from hak.dict.rate.make import f as mk_rate
from hak.pf import f as pf
from hak.puvyz import f as puvyz

def f(u, v):
  if not any([isinstance(u, int), isinstance(u, float)]):
    raise ValueError(f'u: {u} is not a number')

  if not isinstance(v, dict): raise ValueError(f'v: {v} is not a dict')

  return div_rate_by_rate(mk_rate(u, 1, {'1': 0}), v)

def t_a():
  u = 1
  v = mk_rate(1, 3, {'a': 1})
  y = {'numerator': 3, 'denominator': 1, 'unit': {'a': -1}}
  return puvyz(u, v, y, f(u, v))

def t_b():
  u = 5
  v = mk_rate( 7, 9, {'b': 1})
  y = mk_rate(45, 7, {'b': -1})
  return puvyz(u, v, y, f(u, v))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
