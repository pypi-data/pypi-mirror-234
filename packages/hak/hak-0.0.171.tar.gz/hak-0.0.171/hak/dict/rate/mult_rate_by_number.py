from hak.dict.rate.is_a import f as is_rate
from hak.dict.rate.make import f as mk_rate
from hak.number.is_a import f as is_num
from hak.pf import f as pf
from hak.puvyz import f as puvyz

def f(u, v):
  if not is_rate(u): raise ValueError(f'u: {u} is not a rate')
  if not is_num(v): raise ValueError(f'v: {v} is not a number')
  return mk_rate(u['numerator']*v, u['denominator'], u['unit'])

def t_a():
  u = mk_rate(1, 3, {'a': 1})
  v = 1
  return puvyz(u, v, mk_rate(1, 3, {'a': 1}), f(u, v))

def t_b():
  u = mk_rate( 9, 7, {'b': 1})
  v = 5
  return puvyz(u, v, mk_rate(45, 7, {'b': 1}), f(u, v))

def t_c():
  u = mk_rate(1, 3, {'c': 1})
  v = 3
  return puvyz(u, v, mk_rate(1, 1, {'c': 1}), f(u, v))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
