from hak.pxyf import f as pxyf

def f(x):
  observed = set()
  result = []
  for x_i in x:
    if x_i not in observed:
      observed.add(x_i)
      result.append(x_i)
  return result

t = lambda: pxyf(
  [0, 0, 0, 1, 1, 2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 10],
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
  f
)
