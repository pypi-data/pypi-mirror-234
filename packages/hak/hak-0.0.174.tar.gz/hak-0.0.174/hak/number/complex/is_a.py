from hak.bool.random.make import f as make_bool
from hak.number.int.random.make import f as make_int
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.random.make import f as make_str

f = lambda x: type(x) == type(1j)

def t():
  if not pxyf(make_bool(), 0, f): return pf('!t_false_bool')
  if not pxyf(make_int(1, 10), 0, f): return pf('!t_false_int')
  if not pxyf(make_str(), 0, f): return pf('!t_false_str')
  if not pxyf(0+2.5j, 1, f): return pf('!t_true')
  return 1
