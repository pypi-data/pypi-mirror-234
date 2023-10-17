from os.path import isdir
from os.path import isfile
from os import remove

from hak.directory.filepaths.get import f as get_filepaths
from hak.pf import f as pf
from hak.directory.make import f as mkdir
from hak.directory.remove import f as remove_dir
from hak.file.save import f as save

def f(x):
  _packages = set([])
  directories = [_ for _ in get_filepaths(x, []) if isdir(_)]
  for directory in directories:
    python_files_in_directory = [
      _
      for _
      in get_filepaths(directory, [])
      if isfile(_) and _.endswith('.py')
    ]
    if python_files_in_directory: _packages.add(directory)
  return _packages

temp_dir_0 = './_get_packages'
temp_dir_1 = f'{temp_dir_0}/_'
temp_files_and_content = [
  (f'{temp_dir_0}/foo.py', 'foo'),
  (f'{temp_dir_0}/xyz.txt', 'xyz'),
  (f'{temp_dir_1}/abc.txt', 'abc'),
  (f'{temp_dir_1}/bar.py', 'bar'),
]

def up():
  for temp_dir in [temp_dir_0, temp_dir_1]: mkdir(temp_dir)
  for (filename, content) in temp_files_and_content: save(filename, content)

def dn():
  for (filename, _) in temp_files_and_content: remove(filename)
  remove_dir(temp_dir_1)
  remove_dir(temp_dir_0)

def t():
  up()
  y = set([f'{temp_dir_1}'])
  z = set(f(temp_dir_0))
  dn()
  return y == z or pf([f'y: {y}', f'z: {z}'])
