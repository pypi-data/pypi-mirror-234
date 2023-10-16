from datetime import date
from datetime import timedelta
from hak.date.is_a import f as is_date
from random import randint

f = lambda start, end: start + timedelta(days=randint(0, (end - start).days))

def t():
  x = {'start': date(2023, 1, 1), 'end': date(2024, 1, 1)}
  z = f(**x)
  return all([
    x['start'] <= z <= x['end'],
    is_date(z)
  ])
