from hak.rate import Rate as R
from hak.pxyz import f as pxyz

# AUD
f = lambda numerator=0, denominator=1: R(numerator, denominator, {'AUD': 1})

def t():
  x = {'numerator': 1, 'denominator': 2}
  return pxyz(x, R(1, 2, {'AUD': 1}), f(**x))
