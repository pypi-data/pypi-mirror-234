from hak.string.filename.to_module_name import f as get_module_name
from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: sorted([get_module_name(x_i) for x_i in x])

t_c = lambda: pxyf(
  ['./abc/xyz.py', './abc/mno/xyz.py'],
  ['abc.mno.xyz', 'abc.xyz'],
  f
)

def t():
  if not pxyf([], [], f): return pf('!t_a')
  if not pxyf(['./abc/xyz.py'], ['abc.xyz'], f): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
