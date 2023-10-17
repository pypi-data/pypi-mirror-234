# ignore_overlength_lines
from hak.pf import f as pf
from hak.strings.get_last_line_width import f as get_last_line_width
from hak.string.dict.to_limited_width_dict_string import f as dict_string_to_limited_width_dict_string
from hak.pxyf import f as pxyf

def _f(x, w):
  result = ', '.join([f"'{k}': {x[k]}" for k in x])
  while get_last_line_width(result) > w-2:
    result = dict_string_to_limited_width_dict_string(result)
  return result

def f(x, w=80):
  if len(str(x)) <= w: return str(x)
  return '{\n  '+_f(x, w)+'\n}'

t_short = lambda: pxyf(
  {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8},
  "{'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}",
  f
)

t_w = lambda: pxyf(
  {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9},
  "{'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}",
  f
)

t_too_long_a = lambda: pxyf(
  {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 10},
  '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 10",
    "}",
  ]),
  f
)

t_too_long_b = lambda: pxyf(
  {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
    'j': 9, 'k': 10
  },
  '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10",
    "}",
  ]),
  f
)

t_too_long_c = lambda: pxyf(
  {chr(k+97): k for k in range(17)},
  '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16",
    "}",
  ]),
  f
)

t_too_long_d = lambda: pxyf(
  {chr(k+97): k for k in range(18)},
  '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
    "  'r': 17",
    "}",
  ]),
  f
)

t_too_long_e = lambda: pxyf(
  {chr(k+97): k for k in range(26)},
  '\n'.join([
    "{",
    "  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,",
    "  'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,",
    "  'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,",
    "  'z': 25",
    "}",
  ]),
  f
)

def t():
  if not t_short(): return pf('!t_short')
  if not t_w(): return pf('!t_w')
  if not t_too_long_a(): return pf('!t_too_long_a')
  if not t_too_long_b(): return pf('!t_too_long_b')
  if not t_too_long_c(): return pf('!t_too_long_c')
  if not t_too_long_d(): return pf('!t_too_long_d')
  if not t_too_long_e(): return pf('!t_too_long_e')
  return 1
