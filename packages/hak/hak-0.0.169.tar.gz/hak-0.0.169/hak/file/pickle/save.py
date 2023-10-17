from os import mkdir
from os.path import exists
from pickle import dump

from hak.directory.remove import f as rmdir_if_exists
from hak.file.pickle.load_if_exists import f as load_if_exists
from hak.file.remove import f as remove
from hak.pf import f as pf

def f(data, path):
  if '/' in path:
    dir_name = '/'.join(path.split('/')[:-1])
    existed = exists(dir_name)
    if not existed: mkdir(dir_name)
  with open(path, 'wb') as _file: dump(data, _file)

temp_dir_path = './_save'
temp_file_path = f'{temp_dir_path}/x.pickle'
data = {'a': 0, 'b': 1, 'c': {'x': True, 'y': False}}

up = lambda: rmdir_if_exists(temp_dir_path)

dn = lambda: [remove(temp_file_path), rmdir_if_exists(temp_dir_path)]

def t():
  up()
  y = data
  f(data, temp_file_path)
  z = load_if_exists(temp_file_path)
  dn()
  return y == z or pf(['Pickle does not exist failed.', f'y: {y}', f'z: {z}'])
