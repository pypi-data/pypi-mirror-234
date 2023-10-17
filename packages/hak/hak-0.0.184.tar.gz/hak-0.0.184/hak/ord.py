from hak.pxyz import f as pxyz
from hak.rate import Rate as R

class ORD(R):
  def __init__(self, numerator=0, denominator=1):
    super().__init__(numerator, denominator, unit={'ORD': 1})

# ORD
f = lambda x: ORD(**x)
# f = lambda numerator=0, denominator=1: R(numerator, denominator, {'ORD': 1})

def t():
  x = {'numerator': 1, 'denominator': 2}
  y = R(1, 2, {'ORD': 1}).to_dict()
  z = f(x).to_dict()
  return pxyz(x, y, z)
