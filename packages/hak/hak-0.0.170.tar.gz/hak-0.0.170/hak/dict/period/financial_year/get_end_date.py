from datetime import date

from hak.dict.period.financial_year.make import f as mkfy
from hak.pxyf import f as pxyf

# get_ω_date
f = lambda x: date(x['financial_year']['final_year'], 6, 30)

t = lambda: pxyf(
  {'financial_year': mkfy({'start_year': 2022})},
  date(2023, 6, 30),
  f
)
