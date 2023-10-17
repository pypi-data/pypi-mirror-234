from hak.pxyf import f as pxyf
from hak.pf import f as pf
from datetime import date

f = lambda x: date(x.year, x.month, 1)

def t():
  if not pxyf(date(2023, 1, 15), date(2023, 1, 1), f): return pf('!t_a')
  return 1
