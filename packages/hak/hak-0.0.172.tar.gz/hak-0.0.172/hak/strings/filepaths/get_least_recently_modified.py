from os.path import getmtime
from time import sleep

from hak.directory.filepaths.get import f as get_filepaths
from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdir
from hak.file.save import f as save
from hak.pxyz import f as pxyz

def f(x):
  oldest = {'filepath': '', 'time': float('inf')}
  # for filepath in filepaths:
  for filepath in x:
    last_modified_time = getmtime(filepath)
    if last_modified_time < oldest['time']:
      oldest = {'filepath': filepath, 'time': last_modified_time}
  return oldest['filepath']

def up():
  x = {}
  x['dir_name'] = './test_directory_get_most_recently_modified'
  
  # Create test directory
  mkdirine(x['dir_name'])

  # create old file
  x['old_file_content'] = 'ABC'
  x['old_file_path'] = f"{x['dir_name']}/old_file.txt"
  save(x['old_file_path'], x['old_file_content'])

  sleep(1)

  # create new file
  x['new_file_content'] = 'XYZ'
  x['new_file_path'] = f"{x['dir_name']}/new_file.txt"
  save(x['new_file_path'], x['new_file_content'])

  return x

dn = lambda x: rmdir(x['dir_name'])

def t():
  x = up()
  y = x['old_file_path']
  filepaths = get_filepaths(x['dir_name'], [])
  z = f(filepaths)
  dn(x)
  return pxyz(x, y, z)
