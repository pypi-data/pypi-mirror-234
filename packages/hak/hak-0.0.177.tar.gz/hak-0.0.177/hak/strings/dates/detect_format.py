from hak.numbers.ints.mode.get import f as get_mode
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.date.separator.get import f as get_separator
from hak.string.day.is_a import f as is_day
from hak.string.month.is_a import f as is_month
from hak.string.year.is_a import f as is_year

# src.list_strings.dates.detect_format
def f(x):
  year_indices = []
  month_indices = []
  day_indices = []

  for x_i in x:
    a, b, c = x_i.split(get_separator(x_i))

    if is_year(a):
      year_indices.append(0)
      if is_day(b) and not is_day(c):
        day_indices.append(1)
        month_indices.append(2)
      elif not is_day(b) and is_day(c):
        day_indices.append(2)
        month_indices.append(1)
      elif not is_month(b) and is_month(c):
        day_indices.append(1)
        month_indices.append(2)
      elif is_month(b) and not is_month(c):
        day_indices.append(2)
        month_indices.append(1)

    if is_year(b):
      year_indices.append(1)
      if is_day(a) and not is_day(c):
        day_indices.append(0)
        month_indices.append(2)
      elif not is_day(a) and is_day(c):
        day_indices.append(2)
        month_indices.append(0)
      elif not is_month(a) and is_month(c):
        day_indices.append(0)
        month_indices.append(2)
      elif is_month(a) and not is_month(c):
        day_indices.append(2)
        month_indices.append(0)

    if is_year(c):
      year_indices.append(2)
      if is_day(a) and not is_day(b):
        day_indices.append(0)
        month_indices.append(1)
      elif not is_day(a) and is_day(b):
        day_indices.append(1)
        month_indices.append(0)
      elif not is_month(a) and is_month(b):
        day_indices.append(0)
        month_indices.append(1)
      elif is_month(a) and not is_month(b):
        day_indices.append(1)
        month_indices.append(0)

  year_index = get_mode(year_indices)
  month_index = get_mode(month_indices)
  day_index = get_mode(day_indices)

  if not month_index and not day_index:
    if year_index == 2:
      day_index = 0
      month_index = 1
    elif year_index == 1:
      raise NotImplementedError('!A')
    elif year_index == 0:
      day_index = 2
      month_index = 1
    else:
      raise NotImplementedError('!B: Should be impossible')

  return {
    'year_index': year_index,
    'month_index': month_index,
    'day_index': day_index
  }

t_0 = lambda: pxyf(
  ['2021-11-04', '2021/11/19', '2022 01 31'],
  {'year_index': 0, 'month_index': 1, 'day_index': 2},
  f
)

t_1 = lambda: pxyf(
  [
    '28/03/2022',
    '29/03/2022',
    '31/03/2022',
    '5/04/2022',
    '5/04/2022',
    '5/04/2022',
    '5/04/2022',
    '5/04/2022',
    '5/04/2022',
    '5/04/2022',
  ],
  {'year_index': 2, 'month_index': 1, 'day_index': 0},
  f
)

t_2 = lambda: pxyf(
  [
    '2022-05-06',
    '2022-05-06',
    '2022-05-06',
    '2022-05-06',
    '2022-05-06',
    '2022-05-06'
  ],
  {'year_index': 0, 'month_index': 1, 'day_index': 2},
  f
)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  return 1
