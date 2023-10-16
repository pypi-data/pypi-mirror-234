from hak.string.format import f as format_one
from hak.pxyz import f as pxyz

f = lambda x, function=format_one: [function(x_i) for x_i in x]

def t():
  x = {'x': list('abc'), 'function': lambda x: x.capitalize()}
  return pxyz(x, list('ABC'), f(**x))
