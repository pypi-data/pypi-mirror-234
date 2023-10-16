from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  if 'start_year' not in x: return 0
  if 'final_year' not in x: return 0
  if x['final_year'] - x['start_year'] != 1: return 0
  if len(x) != 2: return 0
  return 1

t_0_missing_start_year = lambda: pxyf({'final_year': 2024}, 0, f)
t_0_missing_final_year = lambda: pxyf({'start_year': 2022}, 0, f)
t_0_years_too_far = lambda: pxyf({'start_year': 2022, 'final_year': 2024}, 0, f)
t_0_years_same = lambda: pxyf({'start_year': 2022, 'final_year': 2022}, 0, f)

t_0_has_extra_k = lambda: pxyf(
  {'start_year': 2022, 'final_year': 2023,
  'extra_key': None}, 0,
  f
)

def t():
  if not pxyf({'start_year': 2022, 'final_year': 2023}, 1, f): return pf('!t_1')
  if not t_0_missing_start_year(): return pf('!t_0_missing_start_year')
  if not t_0_missing_final_year(): return pf('!t_0_missing_final_year')
  if not t_0_years_too_far(): return pf('!t_0_years_too_far')
  if not t_0_years_same(): return pf('!t_0_years_same')
  if not t_0_has_extra_k(): return pf('!t_0_has_extra_k')
  return 1
