from hak.strings.filepaths.py.get import f as list_py_files
from hak.directory.make import f as mkdir
from hak.file.save import f as save
from os import remove
from hak.directory.remove import f as remove_dir
from os.path import exists
from hak.pf import f as pf

_f = lambda root='.': [
  φ for φ in list_py_files(root, [])
  if not any([
    φ in [
      './scrap.py',
      './patch.py',
      './test.py',
      './setup.py',
      './temp.py',
      './temp/foo.py',
      './temp/hak.args.py',
      './temp/hak.start.py',
      './temp/hak.app.py',
      './temp/hak.no_comment_present.py',
      './temp/hak.has_comment_to_be_deleted.py',
      './temp/hak.has_comment_to_not_be_deleted.py',
      './fake_setup.py',
      './_pi_test_failed/_expected_fail.py',
      './_pi_test_failed/_expected_pass.py',
      './package_list.py',
      './hak/test/do.py'
    ],
    φ.endswith('__init__.py'),
    φ.endswith('data.py')
  ])
]

def f(root='.'):
  _Pi = _f(root)
  _Pi = [_pi for _pi in _Pi if 'excludables' not in _pi]
  
  for excludable_directory in ['./archive/', './test_data/']:
    _Pi = [_pi for _pi in _Pi if excludable_directory not in _pi]
  
  if exists('excludables.py'):
    from excludables import excludables as _Pi_x
    for _pi_x in _Pi_x:
      _Pi = [_pi for _pi in _Pi if _pi_x not in _pi]
  
  return _Pi

temp_dir_0 = './_'
temp_dir_1 = './_/_'
temp_files_and_content = [
  (f'{temp_dir_0}/foo.py', 'f = lambda: None\nt = lambda: True'),
  (f'{temp_dir_0}/xyz.txt', 'xyz'),
  (f'{temp_dir_1}/abc.txt', 'abc'),
  (f'{temp_dir_1}/bar.py', 'f = lambda: None\nt = lambda: True'),
]

def up():
  [mkdir(temp_dir) for temp_dir in [temp_dir_0, temp_dir_1]]
  [save(filename, content) for (filename, content) in temp_files_and_content]

def dn():
  [remove(filename) for (filename, _) in temp_files_and_content]
  remove_dir(temp_dir_1)
  remove_dir(temp_dir_0)

def t():
  up()
  y = set(['./_/_/bar.py', './_/foo.py'])
  z = set(f(temp_dir_0))
  dn()
  return y == z or pf([f'y: {y}', f'z: {z}'])
