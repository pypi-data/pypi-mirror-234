from hak.pf import f as pf
from hak.pxyf import f as pxyf

# get_empty_fields
def f(x):
  keys_with_values = set([])

  for x_i in x:
    for k in x_i:
      if not any([x_i[k] is None, x_i[k] == 0, x_i[k] == '']):
        keys_with_values.add(k)
 
  return set([k for x_i in x for k in x_i]) - keys_with_values

t_1 = lambda: pxyf([{'a': 'a'}, {'b': 'b'}], set([]), f, new_line=1)
t_2 = lambda: pxyf([{'a': None}, {'b': 'b'}], set(['a']), f, new_line=1)

t_3 = lambda: pxyf(
  [{'a': None}, {'b': 'b'}, {'c': 0}], set(['a', 'c']),
  f,
  new_line=1
)

t_3 = lambda: pxyf(
  [{'a': None}, {'b': 'b'}, {'c': 0}, {'d': ''}], set(['a', 'c', 'd']),
  f,
  new_line=1
)

t_4 = lambda: pxyf(
  [{'a': None}, {'b': 'b'}, {'c': 0}, {'d': ''}, {'d': '!'}], set(['a', 'c']),
  f,
  new_line=1
)

def t():
  if not pxyf([{}, {}], set([]), f, new_line=1): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  if not t_3(): return pf('!t_3')
  if not t_4(): return pf('!t_4')
  return 1
