from hak.puvyz import f as puvyz
from hak.dict.period.financial_year.make import f as mkfy

# gt
f = lambda u, v: u['start_year'] > v['start_year']

def t():
  u = mkfy({'start_year': 2023})
  v = mkfy({'final_year': 2023})
  z = f(u, v)
  return puvyz(u, v, 1, z)
