from hak.pxyf import f as pxyf

# convert_list_of_tuples_to_dict
def f(x):
  Δ = {k: 0 for (k, _) in x}
  for (k, v) in x: Δ[k] += v
  return Δ

t = lambda: pxyf([('a', 1), ('b', 2), ('a', 3), ('b', 4)], {'a': 4, 'b': 6}, f)
