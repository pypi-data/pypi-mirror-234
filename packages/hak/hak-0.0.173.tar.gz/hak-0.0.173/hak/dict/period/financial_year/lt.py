from hak.dict.period.financial_year.make import f as mkfy
from hak.puvyz import f as puvyz

# lt
f = lambda u, v: u['start_year'] < v['start_year']

def t():
  u = mkfy({'start_year': 2021})
  v = mkfy({'final_year': 2023})
  return puvyz(u, v, 1, f(u, v))
