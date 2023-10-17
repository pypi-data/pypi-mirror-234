from datetime import date

from hak.dict.is_a import f as is_dict
from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: sorted(x.keys()) if is_dict(x) else []

t_valid = lambda: pxyf({'z': 0, 'y': 1, 'x': 2}, ['x', 'y', 'z'], f)

def t():
  if not                 t_valid(): return pf('!t_valid')
  if not pxyf(date.today(), [], f): return pf('!t_date')
  return 1
