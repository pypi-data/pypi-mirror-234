from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  result = _f({'': x}, -1, {})
  del result[-1]
  return result

def _f(x, level, result):
  for k in x:
    if level not in result:
      result[level] = set()
    result[level] |= set([k])
    result[level] |= _f(x[k], level+1, result)[level]
  return result

t_a = lambda: pxyf(
  {'k': {'u': {}, 'b': {}}, 'm': {}},
  {0: {'k', 'm'},1: {'u', 'b'}},
  f
)

t_b = lambda: pxyf(
  {'k': {'p': {'s': {}, 'l': {}}, 'k': {}}, 'n': {}},
  {0: {'k', 'n'}, 1: {'p', 'k'}, 2: {'l', 's'}},
  f
)
def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
