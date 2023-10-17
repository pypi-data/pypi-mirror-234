from datetime import date
from datetime import datetime as dt
from time import timezone

from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: dt(x.year, x.month, x.day).timestamp() - timezone

def t():
  if not pxyf(date(1970,1,1),     0, f): return pf('!t_a')
  if not pxyf(date(1970,1,2), 86400, f): return pf('!t_b')
  return 1
