from hak.bools.count_true import f as count_true
from hak.string.has_digit import f as has_09
from hak.string.has_lowercase import f as has_az
from hak.string.has_uppercase import f as has_AZ
from hak.string.has_other_char import f as has_other

f = lambda x: count_true([has_09(x), has_az(x), has_AZ(x), has_other(x)]) >= 3

t = lambda: all([
  not any([
    f('12345678'),
    f('abcdefgh'),
    f('ABCDEFGH'),
    f('!@#$%^&*'),
    f('12345678'),
    f('1234efgh'),
    f('abcdEFGH'),
    f('ABCD%^&*'),
  ]),
  f('12cdEF^&'),
])
