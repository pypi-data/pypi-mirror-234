from hak.pf import f as pf
from hak.pxyf import f as pxyf
from datetime import date

f = lambda x: x.month == 6 and x.day == 30

def t():
  if not pxyf(date(2023, 1,  1), 0, f): return pf('!t_0')
  if not pxyf(date(2023, 6, 30), 1, f): return pf('!t_1')
  return 1
