from hak.pxyf import f as pxyf
from hak.pf import f as pf
from hak.number.int.primes.prime_factors.get import f as g

f = lambda x: set(g(x['numerator'])).intersection(set(g(x['denominator'])))

t_7374_50 = lambda: pxyf({'numerator': 7374, 'denominator': 50}, {2}, f)

def t():
  if not t_7374_50(): return pf('!t_7374_50')
  return 1
