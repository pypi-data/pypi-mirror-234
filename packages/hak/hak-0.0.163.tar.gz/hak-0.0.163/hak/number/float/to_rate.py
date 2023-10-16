from hak.dict.rate.make import f as mk_rate
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# float_to_rate
def f(x):
  d = 10**len(str(x).split('.')[1])
  return mk_rate(round(x*d), d, {})

t_true = lambda: pxyf(
  6.283185307179586,
  {
    'numerator': 3141592653589793,
    'denominator': 500000000000000,
    'unit': {}
  },
  f
)

def t():
  if not t_true(): return pf('!t_true')
  return 1
