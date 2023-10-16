from hak.dict.rate.make import f as mk_rate
from hak.dict.rate.make import f as mk_rate
from hak.dict.rate.to_float import f as to_float
from hak.pxyf import f as pxyf

# __str__
f = lambda x: f"{to_float(x):.2f}"

t = lambda: pxyf(mk_rate(710, 113, {'a': 1}), '6.28', f)
