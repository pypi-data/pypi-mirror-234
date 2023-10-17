from hak.directory.filepaths.get import f as list_filepaths
from hak.directory.make import f as mkdirine
from hak.file.save import f as save
from hak.directory.remove import f as rmdir
from hak.file.remove import f as delete
from hak.directories.empty.remove import f as remove_empty_directories
from hak.directory.is_empty import f as is_empty

_delete_pyc = lambda x: [
  delete(pyc)
  for pyc
  in [
    _ for
    _ in list_filepaths(x, [])
    if _.endswith('.pyc')
  ]
]

def f(x):
  _delete_pyc(x)
  remove_empty_directories(x)

def up():
  x = './hak/directory/temp_dir'
  mkdirine(x)
  for _ in ['foo', 'bar']:
    mkdirine(x+f'/{_}')
    save(x+f'/{_}/a.pyc', f'{_}-a-pyc')
  return x

def dn(x):
  rmdir(x)

def t():
  x = up()
  f(x)
  result = is_empty(x)
  dn(x)
  return result
