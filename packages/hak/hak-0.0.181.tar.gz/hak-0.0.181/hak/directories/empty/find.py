from hak.directories.get import f as get_directories
from hak.directory.is_empty import f as is_empty
from hak.directory.make import f as mkdir
from hak.pxyz import f as pxyz
from hak.directory.remove import f as rmdir

f = lambda root: set([d for d in get_directories(root) if is_empty(d)])

def up():
  _root = './temp_root_B'
  _ = {'x': _root}
  _['temp_directories'] = [f'{_root}/temp_a', f'{_root}/temp_b']
  _['y'] = set([mkdir(x_i) for x_i in _['temp_directories']])
  _['created'] = _['y'] | set([_root])
  return _

def dn(created):
  for d in created:
    rmdir(d)

def t():
  _up = up()
  x = _up['x']
  y = _up['y']
  z = f(x)
  dn(_up['created'])
  return pxyz(x, y, z)
