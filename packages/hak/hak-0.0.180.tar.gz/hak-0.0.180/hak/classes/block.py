from hak.pf import f as pf

class Block:
  def __init__(s, lines):
    s._lines = [l for l in [str(l) for l in lines]]
  
  width = property(lambda s: max([len(l) for l in s._lines]))
  w = property(lambda s: s.width)

  height = property(lambda s: len(s._lines))
  h = property(lambda s: s.height)

  lines = property(lambda s: [f'{l:<{s.w}}' for l in s._lines])

  __str__ = lambda s: '\n'.join(s.lines)

  def append_line(s, line: str):
    s._lines += line.split('\n') if '\n' in line else [line]

  get_line = lambda s, i: s.lines[i]

  __eq__ = lambda u, v: u.lines == v.lines

f = lambda x: Block(x)

t___eq__ = lambda: 1
t___init__ = lambda: 1
t___str__ = lambda: 1
t_append_line = lambda: 1
t_get_line = lambda: 1
t_height = lambda: 1
t_lines = lambda: 1
t_width = lambda: 1

def t():
  if not t___eq__(): return pf('!t___eq__')
  if not t___init__(): return pf('!t___init__')
  if not t___str__(): return pf('!t___str__')
  if not t_append_line(): return pf('!t_append_line')
  if not t_get_line(): return pf('!t_get_line')
  if not t_height(): return pf('!t_height')
  if not t_lines(): return pf('!t_lines')
  if not t_width(): return pf('!t_width')
  return 1
