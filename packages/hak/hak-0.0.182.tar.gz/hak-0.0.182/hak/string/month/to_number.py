from hak.data.months import months
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.string.month.to_number
# to_number
def f(x):
  _x = x.lower()[:3]
  months_list = [m[:3].lower() for m in months]
  if _x in months_list: return months_list.index(_x) + 1
  return int(_x)

def t():
  if not pxyf(     '12', 12, f): return pf('!t_0')
  if not pxyf('January',  1, f): return pf('!t_1')
  return 1
