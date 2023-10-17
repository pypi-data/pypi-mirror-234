from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: {
  'numerator': int(str(x).replace('.', '')),
  'denominator': 10**len(str(x).split('.')[1])
}

t_a = lambda: pxyf(147.48, {'numerator': 14748, 'denominator': 100}, f)
t_b = lambda: pxyf(147.0, {'numerator': 1470, 'denominator': 10}, f)
t_c = lambda: pxyf(0.001, {'numerator': 1, 'denominator': 1000}, f)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
