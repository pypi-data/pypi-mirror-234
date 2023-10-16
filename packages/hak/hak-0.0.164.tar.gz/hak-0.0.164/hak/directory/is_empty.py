from hak.directory.filepaths.get import f as get_filepaths
from hak.directory.make import f as mkdir
from hak.directory.remove import f as rmdir
from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.pxyf import f as pxyf

f = lambda x: len(get_filepaths(root=x, filepaths=[])) <= 0

up = lambda: mkdir('./hak/directory/temp')
dn = lambda x: rmdir(x)

def t_true():
  x = up()
  z = f(x)
  dn(x)
  return pxyz(x, 1, z)

def t():
  if not pxyf('./hak', 0, f): pf('!t_false')
  if not t_true(): pf('!t_true')
  return 1
