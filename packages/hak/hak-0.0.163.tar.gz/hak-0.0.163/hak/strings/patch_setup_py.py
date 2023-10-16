from hak.other.pip.version.to_str import f as make_v_str
from hak.pf import f as pf
from hak.string.contains.version import f as k

_k = lambda x: 'hak/pip/version' not in x

f = lambda v, _L: [
  (f"  version='{make_v_str(v)}'," if k(_l) and _k(_l) else _l) for _l in _L
]

v = {'major': 4, 'minor': 5, 'patch': 6}

def t():
  for (y, z) in [
    ([], f({}, [])),
    ([], f(v, [])),
    (["  version='4.5.6',", '.'], f(v, ["  version='x.x.x',", '.'])),
    (['.', "  version='4.5.6',"], f(v, ['.', "  version='x.x.x',"])),
  ]:
    if y != z: return pf([f'y: {y}', f'z: {z}'])
  return 1
