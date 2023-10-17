from hak.list.is_a import f as is_list
from hak.pf import f as pf
from hak.string.random.make import f as make_random_str

# make_random_list
f = lambda: list(make_random_str())

def t():
  z = [f() for _ in range(2)]
  if z[0] == z[1]: return pf(f'z[0] == z[1]; z[0]: {z[0]}; z[1]: {z[1]};')
  for z_i in z:
    if not is_list(z_i):
      return pf(f'not is_list(z_i); z_i: {z_i}; type(z_i): {type(z_i)};')
  return 1
