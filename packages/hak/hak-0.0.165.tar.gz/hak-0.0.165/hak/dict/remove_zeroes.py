from hak.dict.rate.is_a import f as is_rate
from hak.dict.rate.make import f as mk_rate
from hak.dict.rate.to_float import f as fl
from hak.pf import f as pf
from hak.pxyf import f as pxyf

f = lambda x: {k: x[k] for k in x if (fl(x[k]) if is_rate(x[k]) else x[k]) != 0}

t_1 = lambda: pxyf(
  {'a': 0, 'b': 1, 'rate_a': mk_rate(1, 2, {})},
  {'b': 1, 'rate_a': mk_rate(1, 2, {})},
  f
)

t_2 = lambda: pxyf({'a': 0, 'b': 1, 'rate_a': mk_rate(0, 2, {})}, {'b': 1}, f)

def t():
  if not pxyf({'a': 0, 'b': 1}, {'b': 1}, f): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  return 1
