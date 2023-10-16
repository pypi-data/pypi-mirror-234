from hak.directories.empty.find import f as find_empty_directories
from hak.directory.make import f as mkdir
from hak.directory.remove import f as rmdir
from hak.pxyz import f as pxyz

f = lambda root: set([rmdir(d) for d in find_empty_directories(root)])

def up():
  _root = './temp_root_A'
  _ = {'x': _root}
  _['temp_directories'] = [f'{_root}/temp_a', f'{_root}/temp_b']
  _['y'] = set([mkdir(x_i) for x_i in _['temp_directories']])
  _['created'] = _['y'] | set([_root])
  return _

def dn(x):
  for d in x['created']:
    rmdir(d)

def t():
  _up = up()
  x = _up['x']
  y = _up['y']
  z = f(x)
  dn(_up)
  return pxyz(x, y, z)
