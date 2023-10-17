from random import choice
from string import ascii_letters
from random import randint
from hak.pf import f as pf

# make_random_str
f = lambda charset=ascii_letters, min_length=5, max_length=10: ''.join([
  choice(ascii_letters)
  for _ in range(randint(5, 10))
])

def t():
  _charset = ascii_letters
  _min_length = 5
  _max_length = 10
  x = {
    'charset': _charset,
    'min_length': _min_length,
    'max_length': _max_length,
  }
  z = f(**x)
  if len(z) < _min_length: return pf('len(z) < _min_length')
  if len(z) > _max_length: return pf('len(z) > _max_length')
  for char in z:
    if char not in _charset:
      return pf(f"char: {char} not in _charset: {_charset}")

  return 1
