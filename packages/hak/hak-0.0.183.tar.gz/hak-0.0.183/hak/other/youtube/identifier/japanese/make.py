from hak.data.kana import hiragana
from hak.data.kana import katakana
from hak.data.kana import romaji
from hak.other.youtube.identifier.make import f as gen_id
from hak.pf import f as pf

charset = hiragana+katakana+romaji

# jid_generator
f = lambda size: gen_id(size, charset)

def t():
  x = 3
  z = f(x)
  if len(z) != x: return pf(f"len(z) != x: {len(z)} != {x}")

  for char in z:
    if char not in charset:
      return pf(f"char not in x['chars']: {char} not in {x['chars']}")

  return 1
