from hak.dict.numerator_and_denominator.simplify import f as n_d_simplify
from hak.number.float.to_numerator_denominator import f as float_to_num_den
from hak.number.is_a import f as is_number
from hak.pf import f as pf
from hak.pxyz import f as pxyz

get_decimal_place_count = lambda x: len(str(x).split('.')[1].rstrip('0'))

shift_to_int = lambda x, decimal_place_count: int(x * 10**decimal_place_count)

class Rate:
  def __init__(self, numerator, denominator=None, unit=None):
    if not denominator: denominator = 1
    if not unit: unit = {}
    
    if isinstance(numerator, float):
      a, b = float_to_num_den(numerator).values()
      numerator = a
      denominator *= b
    
    if isinstance(denominator, float):
      a, b = float_to_num_den(denominator).values()
      numerator *= b
      denominator = a
    
    if numerator == 0: denominator = 1

    if isinstance(numerator, float):
      decimal_place_count = len(str(numerator).split('.')[1].rstrip('0'))
      numerator *= 10**decimal_place_count
      denominator *= 10**decimal_place_count
      numerator = int(numerator)
      denominator = int(denominator)

    self._numerator = numerator
    self._denominator = denominator
    self.unit = unit

    self.simplify()

  def simplify(self):
    _dict = n_d_simplify({'numerator': self.n, 'denominator': self.d})
    self._numerator = _dict['numerator']
    self._denominator = _dict['denominator']
    self.unit = self.unit

  n           = property(lambda self: self._numerator)
  numerator   = property(lambda self: self.n)

  d           = property(lambda self: self._denominator)
  denominator = property(lambda self: self.d)

  def __add__(u, v):
    if isinstance(v, Rate):
      if u.unit != v.unit:
        raise ValueError(f"u.unit: {u.unit} != v.unit: {v.unit}")
      return Rate(u.n * v.d + v.n * u.d, u.d * v.d, u.unit)
    elif isinstance(v, (int, float)):
      return u + Rate(v, 1, u.unit)
    else:
      raise TypeError('Unsupported operand type for +')
  
  def __radd__(u, v): return u.__add__(v)

  def __truediv__(u, v):
    _unit = {k: 0 for k in sorted(set(u.unit.keys()) | set(v.unit.keys()))}

    for k in u.unit: _unit[k] += u.unit[k]
    for k in v.unit: _unit[k] -= v.unit[k]

    unit = {k: _unit[k] for k in _unit if _unit[k] != 0}

    return Rate(u._numerator*v.denominator, u._denominator*v.numerator, unit)

  def __str__(self):
    if self._denominator == 0: return f"undefined"
    if self._numerator == 0: return f""
    if self._denominator == 1: return f"{self._numerator}"
    return f"{self._numerator}/{self._denominator}"

  def __sub__(u, v):
    if u.unit != v.unit:
      raise ValueError(f"u.unit: {u.unit} != v.unit: {v.unit}")
    return Rate(u.n * v.d - u.d * v.n, u.d * v.d, u.unit)

  def __mul__(u, v):
    if is_number(v): v = Rate(v, 1, {})

    _unit = {k: 0 for k in sorted(set(u.unit.keys()) | set(v.unit.keys()))}

    for k in u.unit: _unit[k] += u.unit[k]
    for k in v.unit: _unit[k] += v.unit[k]

    return Rate(
      u._numerator  *v._numerator,
      u._denominator*v._denominator,
      {k: _unit[k] for k in _unit if _unit[k] != 0}
    )

  def __eq__(u, v):
    _u = Rate(u.n, u.d, u.unit)
    _v = Rate(v.n, v.d, v.unit)
    return all([_u.n == _v.n, _u.d == _v.d, _u.unit == _v.unit])
  
  __abs__ = lambda s: Rate(abs(s.numerator), abs(s.denominator), s.unit)
  __float__ = lambda self: self.numerator / self.denominator

  def to_dict(self):
    return {'numerator': self.n, 'denominator': self.d, 'unit': self.unit}

  def __repr__(self): return f'Rate(n={self.n}, d={self.d}, unit={self.unit})'

  def __lt__(u, v): return (u - v).n < 0

f = lambda numerator, denominator, unit: Rate(numerator, denominator, unit)

t_u_lt_v = lambda: all([
      Rate(1, 4, {'AUD': 1}) < Rate(1, 3, {'AUD': 1}),
  not Rate(3, 4, {'AUD': 1}) < Rate(2, 3, {'AUD': 1})
])

def t_rate_simplifies_at_init():
  x = {'numerator': 120, 'denominator': 240, 'unit': {'$': 1, 'm': -1}}
  y = Rate(1, 2, {'$': 1, 'm': -1})
  z = Rate(**x)
  return pxyz(x, y, z)

def t_rate_numerator_float():
  x = {'numerator': 0.120, 'denominator': 240, 'unit': {'$': 1, 'm': -1}}
  y = Rate(1, 2000, {'$': 1, 'm': -1})
  z = Rate(**x)
  return pxyz(x, y, z)

def t_rate_denominator_float():
  x = {'numerator': 120, 'denominator': 0.240, 'unit': {'$': 1, 'm': -1}}
  y = Rate(500, 1, {'$': 1, 'm': -1})
  z = Rate(**x)
  return pxyz(x, y, z)

def t_rate_a():
  x = {'numerator': 1, 'denominator': 2, 'unit': {'$': 1, 'm': -1}}
  y = '1/2'
  z = str(Rate(**x))
  return pxyz(x, y, z)

def t_rate_b():
  x = {'numerator': 0, 'denominator': 2, 'unit': {'$': 1, 'm': -1}}
  y = Rate(0, 1, {'$': 1, 'm': -1})
  z = Rate(**x)
  return pxyz(x, y, z)

def t_rate_by_integer():
  x = {'numerator': 2, 'denominator': 3, 'unit': {'$': 1, 'm': -1}}
  x_rate = Rate(**x)
  x_int = 2
  y = Rate(4, 3, {'$': 1, 'm': -1})
  z = x_rate * x_int
  return pxyz(x, y, z)

def t_rate_sum():
  x = [Rate(2, 3, {'$': 1}), Rate(4, 3, {'$': 1})]
  y = Rate(2, 1, {'$': 1})
  z = sum(x)
  return pxyz(x, y, z)

def t_147_48():
  x = {'numerator': 147.48, 'denominator': 1, 'unit': {'AUD': 1}}
  y = Rate(14748, 100, {'AUD': 1})
  return pxyz(x, y, f(**x))

def t():
  if not t_rate_simplifies_at_init(): return pf('!t_rate_simplifies_at_init')
  if not t_rate_numerator_float(): return pf('!t_rate_numerator_float')
  if not t_rate_denominator_float(): return pf('!t_rate_denominator_float')
  if not t_rate_a(): return pf('!t_rate_a')
  if not t_rate_b(): return pf('!t_rate_b')
  if not t_rate_by_integer(): return pf('!t_rate_by_integer')
  if not t_rate_sum(): return pf('!t_rate_sum')
  if not t_147_48(): return pf('!t_147_48')
  if not t_u_lt_v(): return pf('!t_u_lt_v')
  return 1
