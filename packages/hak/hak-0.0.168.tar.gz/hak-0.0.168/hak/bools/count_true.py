from random import randint as u

from hak.pxyf import f as pxyf
from hak.pf import f as pf

f = lambda x: len([_ for _ in x if _])

def t_a():
  n = u(0, 10)
  return pxyf([*[True] * n, False], n, f)

def t_b():
  n = u(0, 10)
  return pxyf([*[1]*n, 0, False], n, f)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not pxyf([], 0, f): return pf('!t_c')
  return 1
