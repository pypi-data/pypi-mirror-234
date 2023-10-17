from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: x['char']*(x['width']+2)

t_minus_3 = lambda: pxyf({'char': '-', 'width': 3}, '-----', f)
t_minus_4 = lambda: pxyf({'char': '-', 'width': 4}, '------', f)
t_space_4 = lambda: pxyf({'char': ' ', 'width': 4}, '      ', f)

def t():
  if not t_minus_3(): return pf('!t_minus_3')
  if not t_minus_4(): return pf('!t_minus_4')
  if not t_space_4(): return pf('!t_space_4')
  return 1
