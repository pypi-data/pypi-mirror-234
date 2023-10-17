from hak.dict.get_or_default import f as get_or_default
from hak.dict.rate.is_a import f as is_rate
from hak.dict.unit.to_str import f as to_str
from hak.pf import f as pf
from hak.pxyz import f as pxyz

# get_unit
def f(k, record):
  v = get_or_default(record, k, {})
  return to_str(v['unit']) if is_rate(v) else ''

def t_a():
  x = {
    'k': 'a',
    'record': {
      'a': {'numerator': 2, 'denominator': 1, 'unit': {'m': 1}},
      'b': {'numerator': 3, 'denominator': 1, 'unit': {'$': 1}}
    }
  }
  return pxyz(x, 'm', f(**x))

def t_b():
  x = {
    'k': 'b',
    'record': {
      'a': {'...': 2, 'denominator': 1, 'unit': {}},
      'b': {'numerator': 3, 'denominator': 2, 'unit': {'$': 1, 'm': -1}}
    }
  }
  return pxyz(x, '$/m', f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
