from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from os.path import exists

temp_root = './_dist_tars_remove'
temp_L = list('abc')

def up(): mkdirine(temp_root)

def dn(): rmdirie(temp_root)

def t():
  up()
  f(temp_L, temp_root)
  result = all([exists(f'{temp_root}/{_l}') for _l in temp_L])
  dn()
  return result

def f(_L, root='.'): [mkdirine(f'{temp_root}/{_l}') for _l in temp_L]
