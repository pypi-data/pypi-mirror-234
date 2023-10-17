from hak.number.float.epsilon import ε
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.float.snap_to_zero
f = lambda x: 0 if abs(x) < 1e-10 else x

def t():
  if not pxyf(-ε, 0, f): return pf('!t_negative_epsilon')
  if not pxyf( 1, 1, f): return pf('!t_one')
  if not pxyf( ε, 0, f): return pf('!t_positive_epsilon')
  if not pxyf( 0, 0, f): return pf('!t_zero')
  return 1
