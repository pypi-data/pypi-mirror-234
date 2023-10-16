from string import ascii_uppercase as _A_to_Z

def f(x):
  if x[:4] == 'den ': return 1
  return all([isinstance(x, str), x[0] in _A_to_Z]) if len(x) else False

t = lambda: all([
  *[f(_) for _ in ['Forbes', 'El Sawah', 'den Hartog', 'Hene Kankanamge']],
  not any([f(_) for _ in ['apple', '' ]])
])
