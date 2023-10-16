from datetime import date
from hak.dict.period.month.get_start_date import f as get_α_d
from hak.dict.period.month.get_end_date import f as get_ω_d
from hak.pf import f as pf

# contains_date
f = lambda x: get_α_d(x) <= x['date'] <= get_ω_d(x)

def t():
  x = {'month': {'year': 2022, 'number': 1}, 'date': date(2022, 1, 10)}
  y = 1
  z = f(x)
  return y == z or pf(f'expected {x["date"]} to be in {x["month"]}')
