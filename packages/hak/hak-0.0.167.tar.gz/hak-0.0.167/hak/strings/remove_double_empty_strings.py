from hak.pxyf import f as pxyf
from hak.pf import f as pf

f = lambda x: (
  [x[i] for i in range(len(x)-1) if any([x[i] != '', x[i+1] != ''])]+
  [x[-1]]
)

t_a = lambda: pxyf(['a', '', '', '', 'b'], ['a', '', 'b'], f)
t_b = lambda: pxyf(['', '', 'b', '', '', 'c'], ['', 'b', '', 'c'], f)
t_c = lambda: pxyf(['', 'c', '', '', 'd'], ['', 'c', '', 'd'], f)
t_d = lambda: pxyf(['', '', 'c', '', '', 'd'], ['', 'c', '', 'd'], f)
t_e = lambda: pxyf(['', '', 'c', '', '', 'd', ''], ['', 'c', '', 'd', ''], f)
t_f = lambda: pxyf(['', 'c', '', '', 'd', '', ''], ['', 'c', '', 'd', ''], f)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  return 1
