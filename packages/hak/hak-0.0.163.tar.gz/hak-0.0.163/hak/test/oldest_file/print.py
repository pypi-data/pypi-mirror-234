from os import remove
from os.path import exists
from os.path import getmtime

from hak.dict.durations.to_tuple_list_sorted_by_duration import f as sort
from hak.file.pickle.load_if_exists import f as load_pickle
from hak.file.pickle.save import f as save_pickle
from hak.file.remove import f as remove
from hak.file.save import f as save
from hak.file.save import f as save_file
from hak.strings.filepaths.py.get import f as list_py_files
from hak.pf import f as pf
from hak.terminal import Terminal
from hak.other.ternary import f as tern

_list_testables = lambda root='.': [
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

def list_testables(root='.'):
  _Pi = _list_testables(root)
  _Pi = [_pi for _pi in _Pi if 'excludables' not in _pi]
  
  for excludable_directory in ['./archive/', './test_data/']:
    _Pi = [_pi for _pi in _Pi if excludable_directory not in _pi]
  
  if exists('excludables.py'):
    from excludables import excludables as _Pi_x
    for _pi_x in _Pi_x:
      _Pi = [_pi for _pi in _Pi if _pi_x not in _pi]
  
  return _Pi

# temp_dir_0 = './_'
# temp_dir_1 = './_/_'
# temp_files_and_content = [
#   (f'{temp_dir_0}/foo.py', 'f = lambda: None\nt = lambda: True'),
#   (f'{temp_dir_0}/xyz.txt', 'xyz'),
#   (f'{temp_dir_1}/abc.txt', 'abc'),
#   (f'{temp_dir_1}/bar.py', 'f = lambda: None\nt = lambda: True'),
# ]

# def up():
#   [mkdir(temp_dir) for temp_dir in [temp_dir_0, temp_dir_1]]
#   [save(filename, content) for (filename, content) in temp_files_and_content]

# def dn():
#   [remove(filename) for (filename, _) in temp_files_and_content]
#   remove_dir(temp_dir_1)
#   remove_dir(temp_dir_0)

# def t():
#   up()
#   y = set(['./_/_/bar.py', './_/foo.py'])
#   z = set(f(temp_dir_0))
#   dn()
#   return y == z or pf([f'y: {y}', f'z: {z}'])

# ------------------------------------------------------------------------------

def make_Pi_t(python_filepaths, test_all, prev, last_mods): return (
  python_filepaths.copy() if test_all else [
    python_filepath
    for python_filepath
    in python_filepaths
    if (
      (prev[python_filepath] if python_filepath in prev else 0) !=
      # tern(     prev[p],      p in prev, 0) !=
      tern(last_mods[python_filepath], python_filepath in last_mods, 0)
    )
  ]
) or python_filepaths.copy()

# _python_filepaths = ['./a.py', './b.py', './c.py']
# _test_all  = False
# _prev = {'./b.py': 32481.8, './c.py': 32497.3}
# _last_mods = {'./a.py': 97551.0, './b.py': 32481.8, './c.py': 32497.3}
# t = lambda: ['./a.py'] == f(_python_filepaths, _test_all, _prev, _last_mods)

# print_oldest_file

# from hak.strings.filepaths.py.testables.get import f as list_testables
# from os.path import getmtime
# from hak.file.pickle.load_if_exists import f as load_pickle
# from hak.file.remove import f as remove
# from hak.file.pickle.save import f as save
# from hak.strings.filepaths.py.testables.get import f as make_Pi_t
# from hak.dict.durations.to_tuple_list_sorted_by_duration import f as sort

# def f(_Pi=None):
#   _Pi = list_testables()
#   try: prev = load_pickle('./last_modified.pickle') or set()
#   except EOFError as _: remove('./last_modified.pickle'); prev = set()
#   last_mods = {py_filename: getmtime(py_filename) for py_filename in _Pi}
#   save(last_mods, './last_modified.pickle')
#   _Pi_fail = set()
#   _A = [_[0] for _ in sort(last_mods)[::-1]]
#   _B = set(make_Pi_t(_Pi, True, prev, last_mods) + list(_Pi_fail))
#   _Pi_t = [a for a in _A if a in _B]
#   print(f'Oldest file: {_Pi_t[-1]}')

def f(filepaths=None, term=None):
  term = term or Terminal()
  
  filepaths = filepaths or list_testables()
  
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  
  last_mods = {py_filename: getmtime(py_filename) for py_filename in filepaths}
  save_pickle(last_mods, './last_modified.pickle')

  python_filepaths_sorted_by_last_mod = [_[0] for _ in sort(last_mods)[::-1]]
  python_filepaths_to_test_and_previously_failed = make_Pi_t(
    filepaths,
    True,
    prev,
    last_mods
  )

  python_filepaths_to_test = [
    python_filepath
    for python_filepath
    in python_filepaths_sorted_by_last_mod
    if python_filepath in python_filepaths_to_test_and_previously_failed
  ]
  oldest = python_filepaths_to_test[-1]
  term.print(f'Oldest file: {oldest}')
  return oldest

def t():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save_file(k, v)
  
  x = list(_test_files.keys())
  y = x[0]
  y_out_stream_list = ['Oldest file: ./a.pz\n']
  term = Terminal(mode='test')
  z = f(x, term=term)
  
  for k in _test_files: remove(k)

  if y != z: return pf(['y != z', f'y: {y}', f'z: {z}'])
  if term.output_stream_as_list != y_out_stream_list: return pf([
    'term.output_stream_as_list != y_out_stream_list',
    f'term.output_stream_as_list: {term.output_stream_as_list}',
    f'y_out_stream_list:          {y_out_stream_list}',
  ])
  return 1
