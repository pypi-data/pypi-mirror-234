from hak.puvyz import f as puvyz
from hak.pf import f as pf

def f(u, v):
  if u == v: return (1, 'Match')
  if len(u) < len(v): return (0, f'len(u): {len(u)} < len(v): {len(v)}')
  if len(u) > len(v): return (0, f'len(u): {len(u)} > len(v): {len(v)}')
  
  for i in range(len(u)):
    if u[i] != v[i]:
      return (0, f"x[{i}]: '{u[i]}' != y[{i}]: '{v[i]}'", i)
  
  return (0, "Unknown mismatch")
  
def t_match():
  u = 'abc'
  v = 'abc'
  return puvyz(u, v, (1, 'Match'), f(u, v))

def t_less():
  u = 'abc'
  v = 'abcd'
  return puvyz(u, v, (0, 'len(u): 3 < len(v): 4'), f(u, v))

def t_greater():
  u = 'abcd'
  v = 'abc'
  return puvyz(u, v, (0, 'len(u): 4 > len(v): 3'), f(u, v))

def t_not_equal():
  u = 'axc'
  v = 'ayc'
  return puvyz(u, v, (0, "x[1]: 'x' != y[1]: 'y'", 1), f(u, v))

def t():
  if not t_match(): return pf('!t_match')
  if not t_less(): return pf('!t_less')
  if not t_greater(): return pf('!t_greater')
  if not t_not_equal(): return pf('!t_not_equal')
  return 1
