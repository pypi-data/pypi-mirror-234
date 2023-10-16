from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.dict.period.financial_year.make import f as mkfy

f = lambda u, v: u['start_year'] <= v['start_year']

def t_expected_true_a():
  x = {'u': mkfy({'start_year': 2022}), 'v': mkfy({'start_year': 2022})}
  return pxyz(x, 1, f(**x))

def t_expected_true_b():
  x = {'u': mkfy({'start_year': 2022}), 'v': mkfy({'start_year': 2024})}
  return pxyz(x, 1, f(**x))

def t_expected_false():
  x = {'u': mkfy({'start_year': 2024}), 'v': mkfy({'start_year': 2022})}
  return pxyz(x, 0, f(**x))

def t():
  if not t_expected_true_a(): return pf('!t_expected_true_a()')
  if not t_expected_true_b(): return pf('!t_expected_true_b()')
  if not t_expected_false(): return pf('!t_expected_false()')
  return 1
