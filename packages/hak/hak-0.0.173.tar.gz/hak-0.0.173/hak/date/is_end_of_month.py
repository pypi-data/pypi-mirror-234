from datetime import date
from hak.number.int.random.make import f as u
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from datetime import timedelta as td

f = lambda x: (x + td(days=1)).day == 1

def t():
  if not pxyf(date(2023, u(1, 12),  u(1, 27)), 0, f): return pf('!t_0')
  if not pxyf(date(2023,  1, 31), 1, f): return pf('!t_01')
  if not pxyf(date(2023,  2, 28), 1, f): return pf('!t_02')
  if not pxyf(date(2023,  3, 31), 1, f): return pf('!t_03')
  if not pxyf(date(2023,  4, 30), 1, f): return pf('!t_04')
  if not pxyf(date(2023,  5, 31), 1, f): return pf('!t_05')
  if not pxyf(date(2023,  6, 30), 1, f): return pf('!t_06')
  if not pxyf(date(2023,  7, 31), 1, f): return pf('!t_07')
  if not pxyf(date(2023,  8, 31), 1, f): return pf('!t_08')
  if not pxyf(date(2023,  9, 30), 1, f): return pf('!t_09')
  if not pxyf(date(2023, 10, 31), 1, f): return pf('!t_10')
  if not pxyf(date(2023, 11, 30), 1, f): return pf('!t_11')
  if not pxyf(date(2023, 12, 31), 1, f): return pf('!t_12')
  if not pxyf(date(2024,  2, 29), 1, f): return pf('!t_02_ly')
  return 1
