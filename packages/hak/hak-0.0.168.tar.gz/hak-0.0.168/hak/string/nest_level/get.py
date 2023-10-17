from hak.pxyf import f as pxyf

def f(x):
  result = []
  nest_level = 0
  for c in x:
    if c == '{':
      result.append(nest_level)
      nest_level += 1
    elif c == '}':
      nest_level -= 1
      result.append(nest_level)
    else:
      result.append(nest_level)
  return result

t = lambda: pxyf(
  str({'a': 0, 'b': 1, 'c': {'d': 0, 'e': 1}}),
  [
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0
  ],
  f
)
