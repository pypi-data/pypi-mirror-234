from ..dict_and_int_divisor.floor_divide import f as floor_div
from .to_common_factors import f as get_common_factors
from hak.pf import f as pf
from hak.pxyf import f as pxyf

_f = lambda n, d: {'numerator': n, 'denominator': d}

def f(x):
  common_factors = get_common_factors(x)
  if common_factors:
    return f(floor_div({'dict': x, 'divisor': common_factors.pop()}))
  return x

def t():
  if not pxyf(_f(2, 4), _f(1, 2), f): return pf('!t_2_4_to_1_2')
  if not pxyf(_f(1, 3), _f(1, 3), f): return pf('!t_1_3_to_1_2')
  if not pxyf(_f(14748, 100), _f(3687, 25), f): return pf('!t_1_3_to_1_2')
  return 1
