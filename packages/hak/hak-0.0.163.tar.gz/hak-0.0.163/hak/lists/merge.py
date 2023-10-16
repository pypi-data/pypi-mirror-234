from hak.pxyz import f as pxyz
from hak.pf import f as pf

f = lambda a, b: a + [b_i for b_i in b if b_i not in set(a)]

def t_a():
  x = {'a': [], 'b': []}
  return pxyz(x, [], f(**x))

def t_b():
  x = {'a': list('abc'), 'b': list('def')}
  return pxyz(x, list('abcdef'), f(**x))

def t_c():
  x = {'a': list('abc'), 'b': list('bcd')}
  return pxyz(x, list('abcd'), f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
