from json import loads
from json import dumps

def f(x):
  try: loads(x)
  except ValueError: return 0
  return 1

t = lambda: all([not f(''), f(dumps({'a': 0, 'b': 1}))])
