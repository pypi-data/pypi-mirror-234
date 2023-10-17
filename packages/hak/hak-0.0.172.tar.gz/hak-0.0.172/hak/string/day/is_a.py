from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.string.day.is_a
# is_year
f = lambda x: 1 <= int(x) <= 31 if x.isdecimal() else False

def t():
  if not pxyf(  'Apr', 0, f): return pf('!t_0')
  if not pxyf('April', 0, f): return pf('!t_1')
  if not pxyf(   '04', 1, f): return pf('!t_2')
  if not pxyf(    '4', 1, f): return pf('!t_3')
  if not pxyf(    '0', 0, f): return pf('!t_4')
  if not pxyf(   '13', 1, f): return pf('!t_5')
  if not pxyf(   '31', 1, f): return pf('!t_6')
  if not pxyf(   '32', 0, f): return pf('!t_7')
  return 1
