from datetime import date
from datetime import timedelta

from hak.dict.period.month.make import f as _m
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# get_ω_date_of_month
f = lambda x: (
  date(
    year=x['month']['year'],
    month=x['month']['number']+1,
    day=1
  ) - timedelta(days=1)
  if x['month']['number'] < 12 else
  date(year=x['month']['year']+1, month=1, day=1) - timedelta(days=1)
)

def t():
  if not pxyf({'month': _m(2016,  5)}, date(2016,  5, 31), f): return pf('!t_0')
  if not pxyf({'month': _m(2017,  6)}, date(2017,  6, 30), f): return pf('!t_1')
  if not pxyf({'month': _m(2020,  2)}, date(2020,  2, 29), f): return pf('!t_2')
  if not pxyf({'month': _m(2021,  2)}, date(2021,  2, 28), f): return pf('!t_3')
  if not pxyf({'month': _m(2021, 12)}, date(2021, 12, 31), f): return pf('!t_4')
  return 1
