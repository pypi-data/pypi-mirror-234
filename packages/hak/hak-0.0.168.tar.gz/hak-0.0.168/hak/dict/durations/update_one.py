from hak.pf import f as pf
from hak.pxyz import f as pxyz

def f(durations, name, δt_ms):
  durations[name] = (
    (durations[name] + δt_ms)/2
    if name
    in durations
    else δt_ms
  )
  return durations

def t_value_update():
  x = {'durations': {'a': 0, 'b': 1}, 'name': 'b', 'δt_ms': 2}
  return pxyz(x, {'a': 0, 'b': 1.5}, f(**x))

def t_value_create():
  x = {'durations': {'a': 0, 'b': 1}, 'name': 'c', 'δt_ms': 2}
  return pxyz(x, {'a': 0, 'b': 1, 'c': 2}, f(**x))

def t():
  if not t_value_update(): return pf('!t_value_update')
  if not t_value_create(): return pf('!t_value_create')
  return 1
