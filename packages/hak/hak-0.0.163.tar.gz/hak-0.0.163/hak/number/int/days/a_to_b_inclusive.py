from datetime import date
from datetime import timedelta as td

f = lambda a, b: ((b - a) + td(days=1)).days

t = lambda: all([
  f(date(2022, 1, 1), date(2022, 1, 1)) == 1,
  f(date(2022, 1, 1), date(2022, 12, 31)) == 365,
])
