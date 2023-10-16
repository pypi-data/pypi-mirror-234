from hak.number.int.is_a import f as is_int
from hak.number.int.primes.prime_factors.get import f as get_prime_factors
from hak.pf import f as pf
from hak.pxyz import f as pxyz

# __init__
def f(numerator, denominator, unit):
  if not isinstance(unit, dict): raise TypeError("not isinstance(unit, dict)")

  if numerator == 0: denominator = 1

  if is_int(numerator) and is_int(denominator):
    numerator_str = str(numerator)
    denominator_str = str(denominator)
    if all([
      numerator_str[-1] == '0',
      denominator_str[-1] == '0',
      len(numerator_str) > 1,
      len(denominator_str) > 1,
    ]):
      numerator_str = numerator_str[:-1]
      denominator_str = denominator_str[:-1]
      numerator = int(numerator_str)
      denominator = int(denominator_str)
      return f(numerator, denominator, unit)

  if '.' in f'{numerator}{denominator}':
    p = len(str(numerator).split('.')[1]) if '.' in str(numerator) else 0
    q = len(str(denominator).split('.')[1]) if '.' in str(denominator) else 0
    u = max(p, q)
    factor = 10**u
    numerator *= factor
    numerator = round(numerator)
    denominator *= factor
    denominator = round(denominator)

  if int(numerator) == numerator: numerator = int(numerator)
  if int(denominator) == denominator: denominator = int(denominator)

  if isinstance(numerator, dict):
    numerator = numerator['numerator']/numerator['denominator']

  if isinstance(numerator, float):
    decimal_place_count = len(str(numerator).split('.')[1].rstrip('0'))
    numerator *= 10**decimal_place_count
    denominator *= 10**decimal_place_count
    numerator = int(numerator)
    denominator = int(denominator)

  npf = get_prime_factors(numerator)
  dpf = get_prime_factors(denominator)

  common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  while common_factors:
    common_factor = common_factors.pop()
    numerator //= common_factor
    denominator //= common_factor
    npf = get_prime_factors(numerator)
    dpf = get_prime_factors(denominator)
    common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  return {'numerator': numerator, 'denominator': denominator, 'unit': unit}

def t_a():
  x = {'numerator': 10, 'denominator': 20, 'unit': {'a': 1}}
  return pxyz(x, {'numerator':  1, 'denominator':  2, 'unit': {'a': 1}}, f(**x))

def t_b():
  x = {'numerator': 0.1, 'denominator': 0.2, 'unit': {'b': 1}}
  return pxyz(x, {'numerator': 1, 'denominator': 2, 'unit': {'b': 1}}, f(**x))

def t_c():
  x = {'numerator': 100, 'denominator': 4, 'unit': {'c': 1}}
  return pxyz(x, {'numerator':  25, 'denominator': 1, 'unit': {'c': 1}}, f(**x))

def t_d():
  x = {'numerator': 25.0, 'denominator': 1, 'unit': {'d': 1}}
  return pxyz(x, {'numerator': 25, 'denominator': 1, 'unit': {'d': 1}}, f(**x))

def t_e():
  x = {'numerator': 80, 'denominator': 4, 'unit': {'e': 1}}
  return pxyz(x, {'numerator': 20, 'denominator': 1, 'unit': {'e': 1}}, f(**x))

def t_f():
  x = {'numerator': 0.7093094658085993, 'denominator': 1, 'unit': {'f': 1}}
  return pxyz(
    x,
    {'numerator': 7093094658085993, 'denominator': 10**16, 'unit': {'f': 1}},
    f(**x)
  )

def t_g():
  x = {'numerator': 5472.0, 'denominator': 7350.89, 'unit': {'g': 1}}
  return pxyz(
    x,
    {'numerator': 547200, 'denominator': 735089, 'unit': {'g': 1}},
    f(**x)
  )

def t_h():
  x = {'numerator': 4491.36, 'denominator': 48, 'unit': {'h': 1}}
  return pxyz(
    x,
    {'numerator': 9357, 'denominator': 100, 'unit': {'h': 1}},
    f(**x)
  )

def t_i():
  x = {
    'numerator': 3293392164473685000,
    'denominator':  2500000000000000,
    'unit': {'i': 1}
  }
  return pxyz(
    x,
    {
      'numerator':     658678432894737,
      'denominator':      500000000000,
      'unit': {'i': 1}
    },
    f(**x)
  )

def t_j():
  x = {'numerator': 0, 'denominator': 10, 'unit': {'j': 1}}
  return pxyz(x, {'numerator': 0, 'denominator':  1, 'unit': {'j': 1}}, f(**x))

def t_k():
  x = {'numerator': 0, 'denominator': 10, 'unit': {}}
  return pxyz(x, {'numerator': 0, 'denominator':  1, 'unit': {}}, f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  if not t_g(): return pf('!t_g')
  if not t_h(): return pf('!t_h')
  if not t_i(): return pf('!t_i')
  if not t_j(): return pf('!t_j')
  if not t_k(): return pf('!t_k')
  return 1
