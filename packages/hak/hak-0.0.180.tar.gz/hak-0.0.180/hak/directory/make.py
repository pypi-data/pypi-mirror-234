from os import mkdir as osmkdir
from os.path import exists

from hak.directory.remove import f as remove
from hak.pf import f as pf

def f(x):
  if exists(x): return x
  try:
    osmkdir(x)
  except FileNotFoundError as fe:
    f('/'.join(x.split('/')[:-1]))
    f(x)
  return x

temp_path_0 = './temp_dir_make'
temp_path_1 = f'{temp_path_0}/_'

def dn():
  remove(temp_path_1)
  remove(temp_path_0)

def t():
  x = temp_path_1
  y_returned = '----'
  z_returned = f(x)
  z_dir_exists = exists(temp_path_1)
  dn()
  if not z_dir_exists: return pf('!z_dir_exists')
  if not z_returned: return pf([
    'z_returned != y_returned',
    f'x: {x}',
    f'y_returned: {y_returned}',
    f'z_returned: {z_returned}'
  ])
  return 1
