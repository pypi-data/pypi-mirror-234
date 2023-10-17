from datetime import date
from hak.pf import f as pf
from hak.pxyf import f as pxyf

_at_least_one_is_none = lambda x: len([_ for _ in x if _ is None])

f = lambda x: (
  0
  if _at_least_one_is_none(x) else
  all([x[0].month == x[i].month for i in range(len(x))])
)

def t():
  if not pxyf((date(2023, 1, 1), date(2023, 2, 1)), 0, f): return pf('!t_0')
  if not pxyf((date(2023, 2, 1), date(2023, 2, 5)), 1, f): return pf('!t_1')
  if not pxyf((None, date(2023, 1, 1)), 0, f): return pf('!t_None')
  return 1
