from datetime import date
# is_monday

def f(δ: date): return δ.weekday() == 0

def t(): return all([
  not f(date(2022, 7, 3)),
  f(date(2022, 7, 4)),
  not f(date(2022, 7, 5)),
  f(date(2022, 7, 11)),
])
