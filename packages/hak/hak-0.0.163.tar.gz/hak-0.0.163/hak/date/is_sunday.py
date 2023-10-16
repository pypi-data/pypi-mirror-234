from datetime import date

# is_sunday
f = lambda x: x.weekday() == 6
t = lambda: all([not f(date(2023, 9, 20)), f(date(2023, 9, 24))])
