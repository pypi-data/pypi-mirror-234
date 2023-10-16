from hak.pxyz import f as pxyz

f = lambda string, char: [i for (i, c) in enumerate(string) if c == char]

def t():
  x = {'string': 'a,b,c,defg', 'char': ','}
  return pxyz(x, [1, 3, 5], f(**x))
