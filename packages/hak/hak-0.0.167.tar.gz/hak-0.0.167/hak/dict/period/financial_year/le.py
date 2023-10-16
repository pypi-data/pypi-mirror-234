from hak.pf import f as pf
from hak.dict.period.financial_year.make import f as mkfy
from hak.puvyz import f as puvyz

# le
f = lambda u, v: u['start_year'] <= v['start_year']

def t_true_a():
  u = mkfy({'start_year': 2022})
  v = mkfy({'final_year': 2023})
  return puvyz(u, v, 1, f(u, v))

def t_true_b():
  u = mkfy({'start_year': 2021})
  v = mkfy({'final_year': 2023})
  return puvyz(u, v, 1, f(u, v))

def t_false():
  u = mkfy({'start_year': 2023})
  v = mkfy({'final_year': 2023})
  return puvyz(u, v, 0, f(u, v))

def t():
  if not t_true_a(): return pf('!t_true_a()')
  if not t_true_b(): return pf('!t_true_b()')
  if not t_false(): return pf('!t_false()')
  return 1
