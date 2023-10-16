from hak.pf import f as pf
from hak.pxyz import f as pxyz

def f(list, item_to_append):
  if item_to_append in list: return list
  return list + [item_to_append]

def t_appended():
  x = {
    'list': ['a', 'b', 'c'],
    'item_to_append': 'd'
  }
  return pxyz(x, ['a', 'b', 'c', 'd'], f(**x))

def t_not_appended():
  x = {
    'list': ['a', 'b', 'c'],
    'item_to_append': 'b'
  }
  return pxyz(x, ['a', 'b', 'c'], f(**x))

def t():
  if not t_appended(): return pf('!t_appended')
  if not t_not_appended(): return pf('!t_not_appended')
  return 1
