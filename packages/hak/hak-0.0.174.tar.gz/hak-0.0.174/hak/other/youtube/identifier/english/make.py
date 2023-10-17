from hak.data.kana import romaji
from hak.pf import f as pf
from hak.other.youtube.identifier.make import f as gen_id

# eid_generator
f = lambda size: gen_id(size, romaji)

def t():
  x = 6
  z = f(x)
  if len(z) != x: return pf(f"len(z) != x: {len(z)} != {x}")

  for char in z:
    if char not in romaji:
      return pf(f"char not in x['chars']: {char} not in {x['chars']}")

  return 1
