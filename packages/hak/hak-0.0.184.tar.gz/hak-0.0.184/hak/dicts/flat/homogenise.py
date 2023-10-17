from hak.dicts.a_into_b import f as a_into_b
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.dict.is_a import f as is_dict

# This works for flat dicts, but not yet for nested ones.

def _update_d_from_dict(d, x_i):
  for k in x_i:
    if k not in d:
      if is_dict(x_i[k]):
        d[k] = dict()
        # d[k] = _update_d_from_dict({}, x_i[k])
      else:
        d[k] = None
  return d

def _build_d_from_dicts(x):
  d = {}
  for x_i in x:
    d = _update_d_from_dict(d, x_i)
  return d

def f(x):
  d = _build_d_from_dicts(x)
  
  y = []
  for x_i in x:
    y.append(a_into_b(x_i, d))
      
  return y

def t_flat():
  x = [
    {'a': 1},
    {'a': 2, 'b': 3},
    {'b': 4}
  ]
  y = [
    {'a':    1, 'b': None},
    {'a':    2, 'b':    3},
    {'a': None, 'b':    4}
  ]
  return pxyf(x, y, f)

def t_nested():
  x = [
    {'a': 1},
    {'a': 2, 'b': {'c': 3}},
    {'b': {'d': 4}}
  ]
  y = [
    {'a':    1, 'b': {'c': None, 'd': None}},
    {'a':    2, 'b': {'c':    3, 'd': None}},
    {'a': None, 'b': {'c': None, 'd':    4}}
  ]
  return pxyf(x, y, f)

def t():
  if not t_flat(): return pf('!t_flat')
  
  # t_nested disabled until f can generalise to nested dicts.
  # if not t_nested(): return pf('!t_nested')

  return 1
