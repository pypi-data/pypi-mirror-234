from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.dict.record_and_keypath.get import f as get_val_from_kp

def f(x):
  try:
    return get_val_from_kp(x)
  except KeyError:
    return x['default']

t_get = lambda: pxyf(
  {'record': {'a': {'b': 0, 'c': 2}}, 'keypath': ('a', 'c'), 'default': 'boo'},
  2,
  f
)

t_default = lambda: pxyf(
  {'record': {'a': {'b': 0, 'c': 2}}, 'keypath': ('a', 'd'), 'default': 'boo'},
  'boo',
  f
)

def t():
  if not t_get(): return pf('!t_get')
  if not t_default(): return pf('!t_default')
  return 1
