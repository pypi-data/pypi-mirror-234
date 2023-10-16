from random import choice
from string import digits

from hak.data.kana import romaji
from hak.pf import f as pf

# id_generator
f = lambda size, chars: ''.join(choice(chars) for _ in range(size))

def t():
  x = {'size': 12, 'chars': romaji + digits+'_!$%'}
  z = f(**x)
  
  if len(z) != x['size']:
    return pf(f"len(z) != x['size']: {len(z)} != {x['size']}")

  for char in z:
    if char not in x['chars']:
      return pf(f"char not in x['chars']: {char} not in {x['chars']}")

  return 1
