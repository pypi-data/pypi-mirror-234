from importlib import import_module
from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from hak.file.save import f as save

f = lambda x: import_module(x.replace('/','.').replace('..','')[:-3]).t

_dir = './_get_t'
_expected_pass_py_filepath = f'{_dir}/_expected_pass.py'
_expected_fail_py_filepath = f'{_dir}/_expected_fail.py'

def up():
  mkdirine(_dir)
  save(_expected_pass_py_filepath, 'f = lambda: None\nt = lambda: True')
  save(_expected_fail_py_filepath, 'f = lambda: None\nt = lambda: False')

def dn(): rmdirie(_dir)

def t():
  up()
  result = all([
    f(_expected_pass_py_filepath)(),
    not f(_expected_fail_py_filepath)()
  ])
  dn()
  return result
