from datetime import date
from datetime import datetime

from hak.bool.is_a import f as is_bool
from hak.date.is_a import f as is_date
from hak.datetime.is_a import f as is_datetime
from hak.dict.is_a import f as is_dict
from hak.dict.rate.is_a import f as is_rate
from hak.dict.rate.make import f as mk_rate
from hak.number.float.is_a import f as is_float
from hak.number.int.is_a import f as is_int
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.set.is_a import f as is_set
from hak.string.is_a import f as is_str
from hak.tuple.is_a import f as is_tup

def f(x):
  if all([is_bool(x_i) for x_i in x]): return 'bool'
  if all([is_datetime(x_i) for x_i in x]): return 'datetime'
  if all([is_date(x_i) for x_i in x]): return 'date'
  if all([is_rate(x_i) for x_i in x]): return 'rate'
  if all([is_dict(x_i) for x_i in x]): return 'dict'
  if all([is_float(x_i) for x_i in x]): return 'float'
  if all([is_int(x_i) for x_i in x]): return 'int'
  if all([is_set(x_i) for x_i in x]): return 'set'
  if all([is_str(x_i) for x_i in x]): return 'str'
  if all([is_tup(x_i) for x_i in x]): return 'tup'
  return '?'

t_bool = lambda: pxyf([True, False, False], 'bool', f)

t_date = lambda: pxyf(
  [date(2023, 1, 1), date(2023, 6, 30), date(2023, 12, 31)],
  'date',
  f
)

t_datetime = lambda: pxyf(
  [datetime(2023, 1, 1), datetime(2023, 6, 30), datetime(2023, 12, 31)],
  'datetime',
  f
)

t_dict = lambda: pxyf([{0: 0}, {1: 1}, {2: 2}], 'dict', f)
t_float = lambda: pxyf([0.0, 1.0, 2.0], 'float', f)
t_int = lambda: pxyf([0, 1, 2], 'int', f)
t_set = lambda: pxyf([set(), set('abc'), {'d', 'e', 'f'}], 'set', f)
t_str = lambda: pxyf(['abc', 'ghi', 'jkl'], 'str', f)
t_tup = lambda: pxyf([('abc', 'ghi'), ('ghi', 'jkl')], 'tup', f)

t_rate = lambda: pxyf(
  [mk_rate(1, 2, {'$': 1, 'm': -1}), mk_rate(2, 3, {'m': 1, '$': -1})],
  'rate',
  f
)

def t_unknown():
  class A:
    pass
  return pxyf([A(), A(), A()], '?', f)

def t():
  if not t_unknown(): return pf('!t_unknown')
  if not t_bool(): return pf('!t_bool')
  if not t_date(): return pf('!t_date')
  if not t_datetime(): return pf('!t_datetime')
  if not t_dict(): return pf('!t_dict')
  if not t_float(): return pf('!t_float')
  if not t_int(): return pf('!t_int')
  if not t_set(): return pf('!t_set')
  if not t_str(): return pf('!t_str')
  if not t_tup(): return pf('!t_tup')
  if not t_rate(): return pf('!t_rate')
  return 1
