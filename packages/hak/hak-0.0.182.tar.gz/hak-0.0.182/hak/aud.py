from hak.rate import Rate as R
from hak.pxyz import f as pxyz

class AUD(R):
  def __init__(self, numerator=0, denominator=1):
    super().__init__(numerator, denominator, unit={'AUD': 1})
  
  def __add__(u, v):
    if isinstance(v, AUD):
      return AUD(u.n * v.d + v.n * u.d, u.d * v.d, u.unit)
    elif isinstance(v, (int, float)):
      return u + AUD(v, 1, u.unit)
    else:
      raise TypeError('Unsupported operand type for +')

  # __str__ = lambda s: (
  #   f'AUD({s.numerator})'
  #   if s.denominator == 1 else
  #   f'AUD({s.numerator}, {s.denominator})'
  # )

# AUD
f = lambda x: AUD(**x)

def t():
  x = {'numerator': 1, 'denominator': 2}
  y = {
    'numerator': 1,
    'denominator': 2,
    'unit': {'AUD': 1}
  }
  z = f(x).to_dict()
  return pxyz(x, y, z)
