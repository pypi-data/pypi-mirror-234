from os import listdir
from os import remove
from os.path import isdir
from os.path import exists

from hak.directory.make import f as mkdir
from hak.directory.remove import f as remove_dir
from hak.file.save import f as save
from hak.pf import f as pf

def f(root, filepaths=[], condition=lambda x: True):
  if exists(root):
    for item in listdir(root):
      _pi = root+'/'+item
      if isdir(_pi): f(_pi, filepaths, condition)
      if condition(item): filepaths.append(_pi)
  return filepaths

def up():
  x = {}
  x['temp_dir_0'] = './_list_filepaths'
  x['temp_dir_1'] = f"{x['temp_dir_0']}/_"
  x['temp_files_and_content'] = [
    (f"{x['temp_dir_0']}/foo.py", 'foo'),
    (f"{x['temp_dir_0']}/xyz.txt", 'xyz'),
    (f"{x['temp_dir_1']}/abc.txt", 'abc'),
    (f"{x['temp_dir_1']}/bar.py", 'bar'),
  ]

  for temp_dir in [x['temp_dir_0'], x['temp_dir_1']]: mkdir(temp_dir)
  for (name, content) in x['temp_files_and_content']: save(name, content)

  x['y'] = set([
    f"{x['temp_dir_0']}/foo.py",
    f"{x['temp_dir_0']}/xyz.txt",
    f"{x['temp_dir_1']}",
    f"{x['temp_dir_1']}/abc.txt",
    f"{x['temp_dir_1']}/bar.py",
  ])
  return x

def dn(x):
  for (filename, _) in x['temp_files_and_content']: remove(filename)
  remove_dir(x['temp_dir_1'])
  remove_dir(x['temp_dir_0'])

def t():
  x = up()
  y = x['y']
  z = set(f(x['temp_dir_0'], []))
  dn(x)
  return y == z or pf([
    f'x: {x}',
    f'y: {y}',
    f'z: {z}',
    f'y-z: {y-z}',
    f'z-y: {z-y}'
  ])
