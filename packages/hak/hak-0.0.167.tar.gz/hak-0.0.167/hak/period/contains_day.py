from datetime import date

f = lambda day, period: period[0] <= day <= period[1]

t = lambda: all([
  f(date(2022,1,1), (date(2022,1,1), date(2022,1,31))),
  f(date(2022,1,15), (date(2022,1,1), date(2022,1,31))),
  f(date(2022,1,31), (date(2022,1,1), date(2022,1,31))),
  not f(date(2022,1,15), (date(2022,2,1), date(2022,1,31)))
])
