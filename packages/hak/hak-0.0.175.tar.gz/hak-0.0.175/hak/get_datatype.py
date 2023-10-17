from datetime import date

from hak.bool.is_a import f as is_bool
from hak.date.is_a import f as is_date
from hak.dict.rate.is_a import f as is_rate
from hak.dict.rate.make import f as mk_rate
from hak.number.complex.is_a import f as is_complex
from hak.number.float.is_a import f as is_float
from hak.number.int.is_a import f as is_int
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.is_a import f as is_str

def f(x):
  if is_str(x): return 'str'
  if is_bool(x): return 'bool'
  if is_int(x): return 'int'
  if is_float(x): return 'float'
  if is_complex(x): return 'complex'
  if is_date(x): return 'date'
  if is_rate(x): return 'rate'
  if x is None: return 'none'
  raise NotImplementedError(f'! This condition not yet considered; x: {x}')

def t():
  if not pxyf('abc', 'str', f): return pf('!t_0')
  if not pxyf(1, 'int', f): return pf('!t_1')
  if not pxyf(1.1, 'float', f): return pf('!t_2')
  if not pxyf(True, 'bool', f): return pf('!t_3')
  if not pxyf(0+1j, 'complex', f): return pf('!t_4')
  if not pxyf(date(2000, 1, 1), 'date', f): return pf('!t_6')
  if not pxyf(mk_rate(2000, 1, {'m': 1}), 'rate', f): return pf('!t_rate')
  if not pxyf(None, 'none', f): return pf('!t_none')
  return 1
