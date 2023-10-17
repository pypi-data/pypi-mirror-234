from hak.string.to_cond_freq_dict import f as to_cond_freq_dict
from hak.dicts.frequencies.merge import f as merge_freq_dicts

def f(x):
  d = {}
  for x_i in x: d = merge_freq_dicts(d, to_cond_freq_dict(x_i))
  return d

def t():
  y = {'aa': {'c': 2, 'd': 1, 'e': 1}, 'ab': {'c': 1, 'd': 1, 'e': 1}}
  z = f(['aac', 'aac', 'aad', 'aae', 'abc', 'abd', 'abe'])
  return y == z
