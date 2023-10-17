from datetime import date

from hak.strings.date_pieces.get import f as get_bag
from hak.strings.date_pieces.separate_day import f as separate_day
from hak.strings.date_pieces.separate_year import f as separate_year
from hak.string.date.separator.get import f as get_separator
from hak.string.month.to_number import f as to_number
from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.pxyf import f as pxyf

# src.string.to_date
def f(x, date_string_format=None):
  if not date_string_format:
    bag = get_bag(x)
    if len(bag) != 3: raise NotImplementedError('!E: len(bag) != 3')
    year, bag = separate_year(bag)
    day, bag = separate_day(bag)
    month = to_number(bag.pop())
    return date(year, month, day)
  
  _ymd = x.split(get_separator(x))

  return date(*[int(_) for _ in [
    _ymd[date_string_format['year_index']],
    _ymd[date_string_format['month_index']],
    _ymd[date_string_format['day_index']]
  ]])

def t_3():
  x = '5/04/2022'
  x_date_string_format = {'year_index': 2, 'month_index': 1, 'day_index': 0}
  return pxyz(x, date(2022, 4, 5), f(x, x_date_string_format))

def t_4():
  x = '2022-05-06'
  x_date_string_format = {'year_index': 0, 'month_index': 1, 'day_index': 2}
  return pxyz(x, date(2022, 5, 6), f(x, x_date_string_format))

def t():
  if not pxyf('19 Nov 2021', date(2021, 11, 19), f): return pf('!t_0')
  if not pxyf('2021-11-19', date(2021, 11, 19), f): return pf('!t_1')
  if not pxyf('28/03/2022', date(2022, 3, 28), f): return pf('!t_2')
  if not t_3(): return pf('!t_3')
  if not t_4(): return pf('!t_4')
  if not f('2016-11-14') == date(2016, 11, 14): return pf('!t_5')
  return 1
