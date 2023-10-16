from hak.pxyf import f as pxyf

# src.list.strings.get_index_of_first_difference
def f(x):
  u = x['u']
  v = x['v']
  for i in range(min(len(u), len(v))):
    if u[i] != v[i]:
      return i

t = lambda: pxyf({'u': 'abcdefghijk', 'v': 'abcdefghiJk'}, 9, f)
