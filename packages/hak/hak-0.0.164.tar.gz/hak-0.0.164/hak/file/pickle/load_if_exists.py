from os.path import exists
from pickle import load
from pickle import dump

from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdir_if_exists
from hak.pf import f as pf

def f(pickle_filename):
  if exists(pickle_filename):
    with open(pickle_filename, 'rb') as _file:
      return load(_file)

temp_dir_path = './temp_pickle_load_if_exists'
temp_file_path = f'{temp_dir_path}/x.pickle'
data = {'a': 0, 'b': 1, 'c': {'x': True, 'y': False}}

def setup_where_pickle_does_not_exist():
  rmdir_if_exists(temp_dir_path)
  mkdirine(temp_dir_path)

def dn(): rmdir_if_exists(temp_dir_path)

def t_where_pickle_does_not_exist():
  setup_where_pickle_does_not_exist()
  y = None
  z = f(temp_file_path)
  dn()
  return y == z or pf(['Pickle not exist case failed.', f'y: {y}', f'z: {z}'])

def setup_where_pickle_exists():
  rmdir_if_exists(temp_dir_path)
  mkdirine(temp_dir_path)
  with open(temp_file_path, 'wb') as _file: dump(data, _file)

def t_where_pickle_exists():
  setup_where_pickle_exists()
  y = data
  z = f(temp_file_path)
  dn()
  return y == z or pf(['Pickle exists case failed.', f'y: {y}', f'z: {z}'])

t = lambda: all([t_where_pickle_does_not_exist(), t_where_pickle_exists()])
