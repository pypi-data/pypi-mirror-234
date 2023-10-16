from hak.dict.is_a import f as is_dict
from hak.pxyf import f as pxyf

def f(d, s=set()):
  for k in d:
    if is_dict(d[k]):
      s |= f(d[k], s)
  return s | set(d.keys())

t = lambda: pxyf(
  {
    'a': {'aa': {'aaa': 'Lollipop'}, 'ab': None},
    'b': {'ba': None}
  },
  set(['a', 'aa', 'ab', 'aaa', 'b', 'ba']),
  f
)
