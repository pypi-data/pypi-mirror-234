from hak.pxyz import f as pxyz
from hak.rate import Rate as R

# ORD
f = lambda numerator=0, denominator=1: R(numerator, denominator, {'ORD': 1})

def t():
  x = {'numerator': 1, 'denominator': 2}
  return pxyz(x, R(1, 2, {'ORD': 1}), f(**x))
