from hak.data.months import months
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.string.month.is_a
# is_month
def f(x):
  x = x.lower()[:3]
  if x in set([m[:3].lower() for m in months]): return 1
  return 1 <= int(x) <= 12 if x.isdecimal() else 0

def t():
  if not pxyf(    '0', 0, f): return pf('!t_0')
  if not pxyf(    '4', 1, f): return pf('!t_1')
  if not pxyf(   '04', 1, f): return pf('!t_2')
  if not pxyf(   '13', 0, f): return pf('!t_3')
  if not pxyf(  'Apr', 1, f): return pf('!t_4')
  if not pxyf('April', 1, f): return pf('!t_5')
  return 1
