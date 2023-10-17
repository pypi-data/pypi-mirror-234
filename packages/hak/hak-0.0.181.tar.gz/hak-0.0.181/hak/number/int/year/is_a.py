from hak.number.int.is_a import f as is_int
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  if not is_int(x): return 0
  if x <= 0: return 0
  if x >= 10000: return 0
  return 1

def t():
  if not pxyf( 2023, 1, f): return pf('!t_true')
  if not pxyf(-2023, 0, f): return pf('!t_false_neg')
  if not pxyf(2000.5, 0, f): return pf('!t_false_float')
  if not pxyf(    0, 0, f): return pf('!t_false_zero')
  if not pxyf(10000, 0, f): return pf('!t_false_too_big')
  return 1
