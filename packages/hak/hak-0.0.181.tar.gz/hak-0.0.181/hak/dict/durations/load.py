from hak.file.pickle.load_if_exists import f as load_if_exists
from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdir_if_exists
from pickle import dump
from hak.pf import f as pf

f = lambda filename='durations.pickle': load_if_exists(filename) or {}

temp_dir_path = './_load_durations_if_exists'
temp_file_path = f'{temp_dir_path}/durations.pickle'
data = {'a': 0, 'b': 1, 'c': 2}

def setup_where_pickle_absent():
  rmdir_if_exists(temp_dir_path)
  mkdirine(temp_dir_path)

def setup_where_pickle_exists():
  setup_where_pickle_absent()
  with open(temp_file_path, 'wb') as _file: dump(data, _file)

dn = lambda: rmdir_if_exists(temp_dir_path)

def t_where_pickle_absent():
  setup_where_pickle_absent()
  z = f(temp_file_path)
  y = {}
  dn()
  return y == z or pf(['pickle absent case failed.', f'y: {y}', f'z: {z}'])

def t_where_pickle_exists():
  setup_where_pickle_exists()
  y = data
  z = f(temp_file_path)
  dn()
  return y == z or pf(['pickle exists case failed.', f'y: {y}', f'z: {z}'])

t = lambda: all([t_where_pickle_absent(), t_where_pickle_exists()])
