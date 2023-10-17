from hak.string.colour.bright.red import f as r
from hak.string.colour.bright.green import f as g
from hak.classes.block import Block

_f = lambda a, b, w, col: [a[j] if a[j]==b[j] else col(a[j]) for j in range(w)]

def f(u, v):
  z_u = []
  z_v = []
  for i in range(u.h):
    x_u_i = u.get_line(i)
    x_v_i = v.get_line(i)
    z_u.append(''.join(_f(x_u_i, x_v_i, u.w, r)))
    z_v.append(''.join(_f(x_v_i, x_u_i, u.w, g)))
  return [Block(z_u), Block(z_v)]

def t():
  u = Block([
    'abc',
    'def',
    'ghi'
  ])
  v = Block([
    'abc',
    'dxf',
    'ghi'
  ])
  x = {'u': u, 'v': v}
  y = [
    Block([
      'abc',
      'd'+r('e')+'f',
      'ghi'
    ]),
    Block([
      'abc',
      'd'+g('x')+'f',
      'ghi'
    ])
  ]
  z = f(**x)
  if y != z:
    print('\n\n'.join([str(y_i) for y_i in y]))
    print('-'*80)
    print('\n\n'.join([str(z_i) for z_i in z]))
    return 0
  return 1
