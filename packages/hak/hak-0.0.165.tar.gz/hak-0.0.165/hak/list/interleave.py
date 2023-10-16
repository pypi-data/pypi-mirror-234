from hak.pxyz import f as pxyz

def f(list, item):
  result = []
  for _ in list:
    result.append(_)
    result.append(item)
  return result[:-1]

def t():
  x = {'list': [0, 1, 2, 3, 4, 5], 'item': 'A'}
  return pxyz(x, [0, 'A', 1, 'A', 2, 'A', 3, 'A', 4, 'A', 5], f(**x))
