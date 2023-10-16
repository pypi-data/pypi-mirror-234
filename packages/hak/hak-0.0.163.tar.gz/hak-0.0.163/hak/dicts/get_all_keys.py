from hak.pxyf import f as pxyf

f = lambda x: sorted(list(set([k for d in x for k in d.keys()])))

t = lambda: pxyf(
  [
    {'a': 1, 'b': 1},
    {'a': 1, 'b': 0},
    {'a': 0, 'b': 0},
    {'a': 0, 'b': 1, 'c': None}
  ],
  ['a', 'b', 'c'],
  f
)
