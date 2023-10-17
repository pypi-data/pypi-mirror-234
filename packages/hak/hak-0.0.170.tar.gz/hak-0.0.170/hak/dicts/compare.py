from hak.pf import f as pf

def f(u, v):
  u_only = {}
  v_only = {}
  in_u_and_v_same_vals = {}
  in_u_and_v_diff_vals = {'u': {}, 'v': {}}

  for k in u:
    if k in v:
      if u[k] == v[k]:
        in_u_and_v_same_vals[k] = u[k]
      else:
        in_u_and_v_diff_vals['u'][k] = u[k]
        in_u_and_v_diff_vals['v'][k] = v[k]
    else:
      u_only[k] = u[k]

  for k in v:
    if k not in u_only:
      if k not in in_u_and_v_same_vals:
        v_only[k] = v[k]

  return {
    'u_only': u_only,
    'v_only': v_only,
    'in_u_and_v_same_vals': in_u_and_v_same_vals,
    'in_u_and_v_diff_vals': in_u_and_v_diff_vals
  }

def t():
  u = {'a': 0, 'b': 1, 'c': 2, 'd': 2}
  v = {                'c': 2, 'd': 3, 'e': 4, 'f': 5}
  y = {
    'u_only': {'a': 0, 'b': 1},
    'v_only': {'d': 3, 'e': 4, 'f': 5},
    'in_u_and_v_same_vals': {'c': 2},
    'in_u_and_v_diff_vals': {'u': {'d': 2}, 'v': {'d': 3}}
  }
  z = f(u, v)
  return y == z or pf([
    f"y['u_only']: {y['u_only']}",
    f"z['u_only']: {z['u_only']}",
    '',
    f"y['v_only']: {y['v_only']}",
    f"z['v_only']: {z['v_only']}",
  ])
