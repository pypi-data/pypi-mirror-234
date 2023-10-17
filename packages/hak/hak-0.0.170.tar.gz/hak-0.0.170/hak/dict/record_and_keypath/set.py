from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  d = x['record']
  k = x['keypath'][0]
  v = x['value']
  d[k] = (
    f({'record': d[k], 'keypath': x['keypath'][1:], 'value': v})
    if len(x['keypath']) > 1 else
    v
  )
  return d

def t_a():
  x = {'record': {'a': {'b': 0, 'c': 2}}, 'keypath': ('a', 'c'), 'value': 3}
  y = {'a': {'b': 0, 'c': 3}}
  return pxyf(x, y, f)

def t():
  if not t_a(): return pf('!t_a')
  return 1
