from string import ascii_lowercase as l
from string import ascii_uppercase as u
from string import digits as d
from string import punctuation as p
from random import choice
from random import shuffle
from hak.string.colour.tgfr import f as tgfr
from hak.pf import f as pf

def f(n=8):
  base = [choice(_) for _ in [d, l, p, u]]
  extra = [choice(l+u+d+p) for _ in range(n-len(base))]
  result = base + extra
  shuffle(result)
  return ''.join(result)

def t():
  z = (f(), f())
  if not isinstance(z[0], str): return pf('not isinstance(z[0], str)')
  has_upper = any([c in u for c in z[0]])
  has_lower = any([c in l for c in z[0]])
  has_digit = any([c in d for c in z[0]])
  has_punct = any([c in p for c in z[0]])
  len_8_plus = len(z[0]) >= 8
  unique = z[0] != z[1]
  result = all([has_upper, has_lower, has_digit, has_punct, len_8_plus, unique])
  return result or pf([
    f'z[0]: {tgfr(z[0])}',
    f'z[1]: {tgfr(z[1])}',
    f'has_upper: {tgfr(has_upper)}',
    f'has_lower: {tgfr(has_lower)}',
    f'has_digit: {tgfr(has_digit)}',
    f'has_punct: {tgfr(has_punct)}',
    f'len_8_plus: {tgfr(len_8_plus)}',
    f'unique: {tgfr(unique)}'
  ])
