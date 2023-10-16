from hak.pxyz import f as pxyz

f = lambda string, char: len(string)-string[::-1].find(char)-1

def t():
  x = {'string': 'a,b,c,de', 'char': ','}
  return pxyz(x, 5, f(**x))
