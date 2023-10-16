from hak.pf import f as pf
from hak.dict.rate.make import f as mk_rate
from hak.pxyz import f as pxyz

def f(x):
  if x['denominator'] == 0: raise ZeroDivisionError('denominator must not be 0')
  if x['denominator'] == 1: return round(x['numerator'])
  return x['numerator']/x['denominator']

def t_int():
  x = mk_rate(2, 1, {'int': 1})
  return pxyz(x, type(2), type(f(x)))

def t_float():
  x = mk_rate(1, 2, {'float': 1})
  return pxyz(x, type(0.5), type(f(x)))

def t():
  if not t_int(): return pf('!t_int')
  if not t_float(): return pf('!t_float')
  return 1
