from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: 'version' in x

def t():
  if not pxyf('xyz version', 1, f): return pf('!t_true_a')
  if not pxyf(    'version', 1, f): return pf('!t_true_b')
  if not pxyf('version xyz', 1, f): return pf('!t_true_c')
  if not pxyf(        'xyz', 0, f): return pf('!t_false_a')
  if not pxyf(           '', 0, f): return pf('!t_false_b')
  return 1
