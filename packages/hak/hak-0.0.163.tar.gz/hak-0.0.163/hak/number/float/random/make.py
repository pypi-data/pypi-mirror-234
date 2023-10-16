from random import random as u

from hak.number.float.is_a import f as is_float
from hak.pf import f as pf

f = lambda: u()

def t():
  z = f()
  if not is_float(z): return pf('!is_float(z)')
  if z < 0: return pf('!z<0')
  if z > 1: return pf('!z>1')
  return 1
