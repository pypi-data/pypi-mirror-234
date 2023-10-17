from datetime import date

from .financial_year.get_start_date import f as f_fy
from .financial_year.make import f as mkfy
from .month.get_start_date import f as get_month_start_date
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.dict.period.month.make import f as _m

# get_α
f = lambda x: (get_month_start_date if 'month' in x else f_fy)(x)

t_a = lambda: pxyf(
  {'financial_year': mkfy({'start_year': 2022})},
  date(2022, 7, 1),
  f
)
t_b = lambda: pxyf(
  {'financial_year': mkfy({'final_year': 2022})},
  date(2021, 7, 1),
  f
)

def t():
  if not pxyf({'month': _m(2016,  5)}, date(2016,  5, 1), f): return pf('!t_0')
  if not pxyf({'month': _m(2017,  6)}, date(2017,  6, 1), f): return pf('!t_1')
  if not pxyf({'month': _m(2020,  2)}, date(2020,  2, 1), f): return pf('!t_2')
  if not pxyf({'month': _m(2021,  2)}, date(2021,  2, 1), f): return pf('!t_3')
  if not pxyf({'month': _m(2021, 12)}, date(2021, 12, 1), f): return pf('!t_4')
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
