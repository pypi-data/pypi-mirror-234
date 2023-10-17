from hak.rate import Rate as R
from hak.pxyz import f as pxyz

class AUD(R):
  def __init__(numerator=0, denominator=1):
    super().__init__(numerator, denominator, unit={'AUD': 1})

  __str__ = lambda s: (
    f'AUD({s.numerator})'
    if s.denominator == 1 else
    f'AUD({s.numerator}, {s.denominator})'
  )

# AUD
f = lambda numerator=0, denominator=1: R(numerator, denominator, {'AUD': 1})

def t():
  x = {'numerator': 1, 'denominator': 2}
  return pxyz(x, R(1, 2, {'AUD': 1}), f(**x))
