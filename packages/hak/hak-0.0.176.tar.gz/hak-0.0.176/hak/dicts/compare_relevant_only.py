from hak.dicts.compare import f as compare
from hak.pf import f as pf

# src.list.dicts.get_relevant_differences
# get_relevant_differences
def f(u, v):
  _c = compare(u, v)
  relevant_keys = set([
    *_c['u_only'].keys(),
    *_c['v_only'].keys(),
    *_c['in_u_and_v_diff_vals'].keys(),
  ])
  return '\n'.join([
    "u: "+str({k: v for (k,v) in u.items() if k in relevant_keys}),
    "v: "+str({k: v for (k,v) in v.items() if k in relevant_keys}),
    'omitted values occurring in both where value is identical'
  ])

def t():
  x_u = {'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}
  x_v = {'b': 'bbb', 'c': 'CCC', 'd': 'ddd'}
  y = '\n'.join([
    "u: {'a': 'aaa', 'c': 'ccc'}",
    "v: {'c': 'CCC', 'd': 'ddd'}",
    "omitted values occurring in both where value is identical"
  ])
  z = f(x_u, x_v)
  return y == z or pf([f'x_u: {x_u}', f'x_v: {x_v}', f'y: {y}', f'z:\n{[z]}'])
