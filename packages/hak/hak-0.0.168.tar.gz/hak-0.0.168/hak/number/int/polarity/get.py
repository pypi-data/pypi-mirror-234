from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: int(x/abs(x) if x else 0)

def t():
  if not pxyf(-123, -1, f): return pf('!t_negative')
  if not pxyf(   0,  0, f): return pf('!t_zero')
  if not pxyf( 123,  1, f): return pf('!t_positive')
  return 1
