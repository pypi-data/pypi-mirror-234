from hak.pf import f as pf
from hak.dict.rate.make import f as mk_rate
from hak.puvyz import f as puvyz

# __eq__
f = lambda u, v: mk_rate(**u) == mk_rate(**v)

def t_true_a():
  u = mk_rate(  1,   2, {'1': 0})
  v = mk_rate(1.0, 2.0, {'1': 0})
  return puvyz(u, v, 1, f(u, v))

def t_true_b():
  u = mk_rate( 0.25, 0.5, {'1': 0})
  v = mk_rate(10, 20, {'1': 0})
  return puvyz(u, v, 1, f(u, v))

def t_false():
  u = mk_rate(1, 2, {'1': 0})
  v = mk_rate(2, 3, {'1': 0})
  return puvyz(u, v, 0, f(u, v))

def t_false_different_units():
  u = mk_rate(1, 2, {'a': 1})
  v = mk_rate(2, 3, {'b': 1})
  return puvyz(u, v, 0, f(u, v))

def t():
  if not t_true_a(): return pf('!t_true()')
  if not t_true_b(): return pf('!t_true()')
  if not t_false(): return pf('!t_false()')
  if not t_false_different_units(): return pf('!t_false_different_units')
  return 1
