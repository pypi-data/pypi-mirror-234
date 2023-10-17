from datetime import date
# is_first_week_of_quarter

def f(δ:date): return δ.month in [1, 4, 7, 10] and δ.day < 8

def t(): return all([
  *[f(date(2022, m, 1)) for m in [1, 4, 7, 10]],
  *[f(date(2022, m, 7)) for m in [1, 4, 7, 10]],
  *[not f(date(2022, m, 8)) for m in [1, 4, 7, 10]],
  *[not f(date(2022, m, 12)) for m in [1, 4, 7, 10]],
  *[not f(date(2022, m, 2)) for m in [2, 3, 5, 6, 8, 9, 11, 12]]
])
