from hak.pxyz import f as pxyz

f = lambda x: all([x%i for i in range(2, x)])

def t():
  for (x, y) in [
    *[(_, False) for _ in [4, 6, 8, 9, 10, 12, 14, 15, 16, 180]],
    *[(_, True) for _ in [2, 3, 5, 7, 11, 13, 17]]
  ]:
    z = f(x)
    if y != z: return pxyz(x, y, z)
  return 1
