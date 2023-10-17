from hak.number.int.year.days.first.get import f as d

f = lambda x: (d(x+1)-d(x)).days

t = lambda: f(2022) == 365 and f(2020) == 366
