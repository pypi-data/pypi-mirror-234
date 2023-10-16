from hak.other.pip.version.to_str import f as make_v_str
from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.string.contains.version import f as k

f = lambda version, lines: [
  (f"  version='{make_v_str(version)}'," if k(l) else l) for l in lines
]

v = {'major': 4, 'minor': 5, 'patch': 6}

def t_a():
  x = {'version': {}, 'lines': []}
  return pxyz(x, [], f(**x))

def t_b():
  x = {'version': v, 'lines': []}
  return pxyz(x, [], f(**x))

def t_c():
  x = {'version': v, 'lines': ["version = '1.2.3'\n", '.\n']}
  return pxyz(x, ["  version='4.5.6',", '.\n'], f(**x))

def t_d():
  x = {'version': v, 'lines': ['.\n', "version = '1.2.3'\n"]}
  return pxyz(x, ['.\n', "  version='4.5.6',"], f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  return 1
