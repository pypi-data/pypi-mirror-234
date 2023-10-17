f = lambda x: any([' = lambda self' in x, ' = lambda:' in x, ' = lambda ' in x])

t = lambda: all([
  not f('abc'),
  f('abc = lambda self'),
  f('f = lambda:'),
  f('f = lambda '),
  f('t = lambda:'),
  f('t = lambda ')
])
