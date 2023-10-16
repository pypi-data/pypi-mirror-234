from os.path import exists
from os.path import isdir
from hak.directory.make import f as mkdirine
from hak.file.save import f as save
from hak.directory.remove import f as rmdirie

_dir = './_directory_is_module'

_dir_expected_true = f'{_dir}/_expected_true'
_dir_expected_false = f'{_dir}/_expected_false'

def up():
  mkdirine(_dir)
  mkdirine(_dir_expected_true)
  save(f'{_dir_expected_true}/__init__.py', '')
  mkdirine(_dir_expected_false)

def dn(): rmdirie(_dir)

f = lambda x: all([exists(x), isdir(x), exists(f'{x}/__init__.py')])

def t():
  up()
  result = all([f(_dir_expected_true), not f(_dir_expected_false)])
  dn()
  return result
