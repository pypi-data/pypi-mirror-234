from hak.fake.printer import f as FP

# print_and_return_false
def f(x, p=print, silent=False):
  if silent: return 0
  if isinstance(x, list): x = '\n'.join(x)
  p(x)
  return 0

def t_0():
  _fake_printer = FP()
  return all([not f('abc', _fake_printer), _fake_printer.history[0] == 'abc'])

def t_1():
  _fake_printer = FP()
  return all([
    not f(['abc', '123', 'xyz'], _fake_printer),
    _fake_printer.history[0] == 'abc\n123\nxyz'
  ])

def t_silent():
  _fake_printer = FP()
  return all([
    not f('abc', _fake_printer, silent=True),
    _fake_printer.history == []
  ])

def t():
  if not t_0(): print("!t_0"); return 0
  if not t_1(): print("!t_1"); return 0
  if not t_silent(): print("!t_silent()"); return 0
  return 1
