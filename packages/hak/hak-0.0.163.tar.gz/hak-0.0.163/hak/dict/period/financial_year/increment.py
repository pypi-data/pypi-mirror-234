from hak.pf import f as pf
from hak.dict.period.financial_year.make import f as mkfy
from hak.pxyf import f as pxyf

# increment
f = lambda x: mkfy({'final_year': x['final_year']+1})

t_a = lambda: pxyf(mkfy({'start_year': 2022}), mkfy({'start_year': 2023}), f)

def t():
  if not t_a(): return pf('!t_a')
  return 1
