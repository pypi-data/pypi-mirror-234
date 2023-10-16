from hak.string.colour.bright.green import f as green
from hak.string.colour.decolour import f as decolour
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  v = str(x['value'])
  δ = len(v) - len(decolour(v))
  w = x['width'] + δ
  return f" {v:>{w}} "

t_int = lambda: pxyf({'value': 12, 'width': 10}, '         12 ', f)
t_yes = lambda: pxyf({'value': green('Y'), 'width': 4}, f"    {green('Y')} ", f)

def t():
  if not t_int(): return pf('!t_int')
  if not t_yes(): return pf('!t_yes')
  return 1
