from hak.pf import f as pf
from hak.pxyz import f as pxyz

f = lambda string, char: len(string) - len(string.replace(char, ''))

def t_a():
  x = {'string': 'a', 'char': ' ' }
  return pxyz(x, 0, f(**x))

def t_b():
  x = {'string': 'a b', 'char': ' ' }
  return pxyz(x, 1, f(**x))

def t_c():
  x = {'string': 'a b c', 'char': ' ' }
  return pxyz(x, 2, f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
