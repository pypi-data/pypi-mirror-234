from hak.pf import f as pf
from hak.pxyz import f as pxyz

def f(x):
  x['start_year'] = x['start_year'] if 'start_year' in x else None
  x['final_year'] = x['final_year'] if 'final_year' in x else None

  if x['start_year'] is None and x['final_year'] is None:
    raise ValueError('Please specify inital_year or final_year')
  
  if x['start_year'] is None and x['final_year'] is not None:
    x['start_year'] = x['final_year'] - 1
  
  if x['start_year'] is not None and x['final_year'] is None:
    x['final_year'] = x['start_year'] + 1

  if x['final_year'] - x['start_year'] != 1: raise ValueError(
    'Years should be contiguous, where start_year precedes final_year.'
  )
  return x

def t_a():
  x = {'start_year': 2022}
  z = f(x)

  if z["start_year"] != 2022: return pf('z["start_year"] != 2022')
  if z["final_year"] != 2023: return pf('z["final_year"] != 2023')  
  return pxyz(x, {'start_year': 2022, 'final_year': 2023}, z)

def t_α_and_final_are_1_year_apart():
  z = f({'final_year': 2022})
  return z["final_year"] - z["start_year"] == 1

def t_illegal_α_final_years_combination():
  try:
    f({'start_year': 2000, 'final_year': 2002})
  except ValueError as ve:
    if str(ve) != (
      'Years should be contiguous, where start_year precedes final_year.'
    ):
      return pf(
        "str(ve) != 'Years should be contiguous, "
        "where start_year precedes final_year.'"
      )
  return 1

def t():
  if not t_a(): return pf('!t_a')

  if not t_α_and_final_are_1_year_apart():
    return pf('!t_α_and_final_are_1_year_apart()')

  if not t_illegal_α_final_years_combination():
    return pf('t_illegal_α_final_years_combination')

  return 1
