from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.string.money.to_float
f = lambda x: float(x.strip().replace('$', '')) if x else 0.0

def t():
  if not pxyf(         '',   0.0, f): return pf('!t_0')
  if not pxyf(' $200.00 ', 200.0, f): return pf('!t_1')
  if not pxyf('$ 300.00 ', 300.0, f): return pf('!t_2')
  return 1
