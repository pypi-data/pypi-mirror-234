from hak.pf import f as pf
from hak.pxyf import f as pxyf

# is_0
f = lambda x: f"{x}" == '0'

def t():
  if not pxyf(1, 0, f): return pf('!t_0')
  if not pxyf(0, 1, f): return pf('!t_1')
  return 1
