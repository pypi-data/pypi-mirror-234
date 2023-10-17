from datetime import date

from hak.dict.period.financial_year.make import f as mkfy
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# get_α_date
f = lambda x: date(x['financial_year']['start_year'], 7, 1)

t_a = lambda: pxyf(
  {'financial_year': mkfy({'start_year': 2022})},
  date(2022, 7, 1),
  f
)

t_b = lambda: pxyf(
  {'financial_year': mkfy({'final_year': 2022})},
  date(2021, 7, 1),
  f
)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return 1
