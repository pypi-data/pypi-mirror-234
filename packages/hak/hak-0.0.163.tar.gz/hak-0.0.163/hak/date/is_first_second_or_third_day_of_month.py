# is_first_second_or_third_day_of_month
from random import randint
from datetime import date

def f(δ: date): return 0 < δ.day < 4

def t(): return all([
  f(date(2022, randint(1, 12), 1)),
  f(date(2022, randint(1, 12), 2)),
  f(date(2022, randint(1, 12), 3)),
  not f(date(2022, randint(1, 12), 4)),
  not f(date(2022, randint(1, 12), 5)),
])
