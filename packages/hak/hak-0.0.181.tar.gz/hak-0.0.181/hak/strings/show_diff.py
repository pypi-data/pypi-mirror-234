from hak.puvyz import f as puvyz
from hak.string.colour.bright.cyan import f as cy
from hak.string.colour.bright.magenta import f as mg
from hak.string.colour.bright.yellow import f as yl
from hak.strings.find_first_diff import f as find_first_diff

# show_diff

def f(u, v, w=64):
  u = str(u)
  v = str(v)
  i = find_first_diff(u, v)['i']
  return [
    str(i),
    cy(u[i-w:i]) + yl(u[i]) + cy(u[i+1:i+w]),
    mg(v[i-w:i]) + yl(v[i]) + mg(v[i+1:i+w]),
  ]

def t():
  u = 'abcdef'
  v = 'abxdef'
  return puvyz(
    u,
    v,
    [
      '2',
      '\x1b[1;36mab\x1b[0;0m\x1b[1;33mc\x1b[0;0m\x1b[1;36mdef\x1b[0;0m',
      '\x1b[1;35mab\x1b[0;0m\x1b[1;33mx\x1b[0;0m\x1b[1;35mdef\x1b[0;0m'
    ],
    f(u, v)
  )
