from hak.pxyf import f as pxyf

def f(x):
  w = max([len(l) for l in x])
  return [(l+' '*w)[:w] for l in x]

def t():
  x = [
    'AAAA',
    'BBB',
    'CC',
    'D',
    '',
    'E'
  ]
  y = [
    'AAAA',
    'BBB ',
    'CC  ',
    'D   ',
    '    ',
    'E   '
  ]
  return pxyf(x, y, f)
