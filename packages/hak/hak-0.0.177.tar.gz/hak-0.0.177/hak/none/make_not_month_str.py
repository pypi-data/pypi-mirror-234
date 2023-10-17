from random import choice

from hak.data.months import months
from hak.string.random.make import f as random_string
from hak.data.months import extended_names_as_set

# make_not_month_str
def f():
  y = choice(months)
  while y in extended_names_as_set:
    y = random_string(min_length=3, max_length=9)
  return y

t = lambda: f() not in extended_names_as_set
