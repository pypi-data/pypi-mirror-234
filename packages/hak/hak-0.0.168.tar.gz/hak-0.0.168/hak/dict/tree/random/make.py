from random import random as u
from hak.string.char.random_az import f as u_az
from hak.dict.is_a import f as is_dict

def f(v, decay=0.5):
  if u() <= v:
    v *= decay
    obj = {}
    while u() <= v:
      obj[u_az()] = f(v)
    return obj
  else:
    return {}

def t():
  x = {'v': 1, 'decay': 0.9}
  z = f(**x)
  return is_dict(z)
