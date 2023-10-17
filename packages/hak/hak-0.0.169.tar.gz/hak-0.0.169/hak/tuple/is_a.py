f = lambda x: isinstance(x, tuple)

t = lambda: all([
  f((None,)),
  f(('a',)),
  f(('a', 'b')),
  f(('a', None)),
  f((1, 2)),
  not any([f(_) for _ in [0, 1.5, [], '']])
])
