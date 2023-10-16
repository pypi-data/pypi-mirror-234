from hak.pf import f as pf
from hak.dict.rate.make import f as mk_rate
from hak.dict.rate.is_a import f as is_rate
from hak.puvyz import f as puvyz

def f(u, v):
  if not is_rate(u): raise ValueError(f'u: {u} is not a rate')
  if not is_rate(v): raise ValueError(f'v: {v} is not a rate')

  _unit = {k: 0 for k in sorted(set(u['unit'].keys()) | set(v['unit'].keys()))}

  for k in u['unit']: _unit[k] += u['unit'][k]
  for k in v['unit']: _unit[k] += v['unit'][k]

  return mk_rate(
    u[  'numerator']*v[  'numerator'],
    u['denominator']*v['denominator'],
    {k: _unit[k] for k in _unit if _unit[k] != 0}
  )

def t_a():
  u = mk_rate( 1,  3, {'m': 1})
  v = mk_rate( 3,  1, {'m': 1})
  return puvyz(u, v, mk_rate(1, 1, {'m': 2}), f(u, v))

def t_b():
  u = mk_rate( 2,  3, {'s': 1})
  v = mk_rate( 5,  7, {'s': 1})
  return puvyz(u, v, mk_rate(10, 21, {'s': 2}), f(u, v))

def t_c():
  u = mk_rate(13, 11, {})
  v = mk_rate(19, 17, {})
  return puvyz(u, v, mk_rate(247, 187, {}), f(u, v))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1
