from datetime import date

from hak.dict.rate.is_a import f as is_a_rate
from hak.dict.rate.make import f as mk_rate
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# detect_datatype_from_values
def f(values):
  # consider whether field contains rate dicts
  if all([is_a_rate(v) for v in values if v]): return 'rate'

  _types = set([type(_) for _ in values])
  if type(None) in _types: _types.remove(type(None))
  # if len(_types) > 1: return 'mixed'
  
  _type = _types.pop()
  if   _type == type('abc'): return 'str'
  elif _type == type(1): return 'int'
  elif _type == type(1.0): return 'float'
  elif _type == type(True): return 'bool'
  elif _type == type(1j): return 'complex'
  elif _type == type(mk_rate(1, 1, {})): return 'rate'
  elif _type == type(date.today()): return 'date'
  else:
    print(f'values: {values}')
    print(f'_type: {_type}')
    raise NotImplementedError('Code not written for this type yet.')

t_5 = lambda: pxyf([
  mk_rate(110, 72, {}),
  mk_rate(72, 111, {}), None],
  'rate',
  f
)

t_6 = lambda: pxyf([date(2000, 1, 1), date(2001, 1, 1)], 'date', f)

t_rate = lambda: pxyf(
  [mk_rate(2000, 1, {'m': 1}), mk_rate(2001, 1, {'m': 1}), None],
  'rate',
  f
)

def t():
  if not pxyf(['abc', 'xyz', None], 'str', f): return pf('!t_0')
  if not pxyf([1, 2, None], 'int', f): return pf('!t_1')
  if not pxyf([1.1, 2.2, None], 'float', f): return pf('!t_2')
  if not pxyf([True, False, None], 'bool', f): return pf('!t_3')
  if not pxyf([0+1j, 1+0j, None], 'complex', f): return pf('!t_4')
  if not t_5(): return pf('!t_5')
  if not t_6(): return pf('!t_6')
  if not t_rate(): return pf('!t_rate')
  return 1
