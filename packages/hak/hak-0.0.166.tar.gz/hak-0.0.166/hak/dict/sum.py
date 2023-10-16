from hak.dict.is_a import f as g
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.rate import Rate as Q

f = lambda x: sum([f(x[k]) if g(x[k]) else x[k] for k in x]) if g(x) else x

t_ints  = lambda: pxyf({'c': {'d': 2, 'e': 3, 'f': {'g': 4, 'h': 5}}},    14, f)
t_rates = lambda: pxyf(      {'b': Q(1), 'c': {'d': Q(2), 'e': Q(3)}},  Q(6), f)
t_rate  = lambda: pxyf(                                          Q(1),  Q(1), f)

def t():
  if not t_ints(): return pf('!t_ints')
  if not t_rates(): return pf('!t_rates')
  if not t_rate(): return pf('!t_rate')
  return 1
