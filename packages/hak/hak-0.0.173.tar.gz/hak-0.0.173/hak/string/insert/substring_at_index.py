# ignore_overlength_lines
from hak.pxyz import f as pxyz
from hak.pf import f as pf

f = lambda string, substring, index: string[:index]+substring+string[index:]

def t_0():
  x = {
    'string': 'abcdef',
    'substring': '---',
    'index': 3
  }
  return pxyz(x, 'abc---def', f(**x))

def t_1():
  x = {
    'string': '\n'.join([
      "'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
      "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
      "  'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25"
    ]),
    'substring': '\n ',
    'index': 218
  }
  return pxyz(
    x,
    '\n'.join([
      "'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
      "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
      "  'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,",
      "  'z': 25"
    ]),
    f(**x)
  )

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  return 1
