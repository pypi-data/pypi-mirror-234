f = lambda x: isinstance(x, dict)

t = lambda: all([
  not any([f(_) for _ in [
    'abc',
    '',
    0,
    [],
    ['ab', 'cd'],
    [{'a': 0}, {'b': 1}]
  ]]),
  f({'a': 0, 'b': 1}),
])
