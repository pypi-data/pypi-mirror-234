from datetime import date

from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.dict.period.month.make import f as _m

# get_first_date_of_month
f = lambda x: date(year=x['month']['year'], month=x['month']['number'], day=1)

def t():
  if not pxyf({'month': _m(2016,  5)}, date(2016,  5, 1), f): return pf('!t_0')
  if not pxyf({'month': _m(2017,  6)}, date(2017,  6, 1), f): return pf('!t_1')
  if not pxyf({'month': _m(2020,  2)}, date(2020,  2, 1), f): return pf('!t_2')
  if not pxyf({'month': _m(2021,  2)}, date(2021,  2, 1), f): return pf('!t_3')
  if not pxyf({'month': _m(2021, 12)}, date(2021, 12, 1), f): return pf('!t_4')
  return 1
