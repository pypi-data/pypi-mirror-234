from hak.pf import f as pf
from hak.pxyf import f as pxyf

# is_none
f = lambda x: x is None

def t():
  if not pxyf(   0, 0, f): return pf('!t_0')
  if not pxyf(None, 1, f): return pf('!t_1')
  return 1
