from hak.pxyz import f as pxyz
from hak.pf import f as pf
from hak.dict.is_a import f as is_dict

f = lambda x, q: max([0] + [f(x[k], q+1) if is_dict(x[k]) else q+1 for k in x])

def t_0():
  x = dict()
  y = 0
  z = f(x, 0)
  return pxyz(x, y, z)

def t_1():
  x = {'a': 0}
  y = 1
  z = f(x, 0)
  return pxyz(x, y, z)

def t_2_a():
  x = {'a': {'a': 0}}
  y = 2
  z = f(x, 0)
  return pxyz(x, y, z)

def t_2_b():
  x = {'a': {'a': 0, 'b': 0}}
  y = 2
  z = f(x, 0)
  return pxyz(x, y, z)

def t_3():
  x = {'a': {'a': {'a': 0}, 'b': 0}}
  y = 3
  z = f(x, 0)
  return pxyz(x, y, z)

def t_4():
  x = {'a': {'a': {'a': {'a': 0}}, 'b': 0}}
  y = 4
  z = f(x, 0)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2_a(): return pf('!t_2_a')
  if not t_2_b(): return pf('!t_2_b')
  if not t_3(): return pf('!t_3')
  return 1
