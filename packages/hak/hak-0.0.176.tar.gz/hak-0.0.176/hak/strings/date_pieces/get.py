from hak.string.date.separator.get import f as get_separator
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# src.string.date_pieces.get
# get_bag
f = lambda x: set(x.split(get_separator(x)))

def t():
  if not pxyf('19 Nov 2021', set([  '19', 'Nov', '2021']), f): return pf('!t_0')
  if not pxyf( '2021-11-19', set(['2021',  '11',   '19']), f): return pf('!t_1')
  if not pxyf( '28/03/2022', set(['2022',  '03',   '28']), f): return pf('!t_2')
  return 1
