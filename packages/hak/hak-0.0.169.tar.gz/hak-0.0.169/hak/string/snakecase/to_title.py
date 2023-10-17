from hak.pxyf import f as pxyf

f = lambda x: x.title().replace('_', ' ')

def t():
  x = 'aa_bb_cc'
  y = 'Aa Bb Cc'
  return pxyf(x, y, f)
