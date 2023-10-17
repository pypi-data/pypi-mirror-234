from os.path import getmtime
from time import time

from hak.dict.durations.to_tuple_list_sorted_by_duration import f as sort
from hak.file.pickle.load_if_exists import f as load_pickle
from hak.file.pickle.save import f as save
from hak.file.remove import f as remove
from hak.strings.filepaths.py.testables.get import f as list_testables
from hak.strings.filepaths.py.to_filepath_file_content_dict import f as pyfiles_to_dict
from hak.string.colour.bright.red import f as danger
from hak.string.colour.dark.yellow import f as warn
from hak.string.contains.function.run import f as has_f
from hak.string.contains.function.test import f as has_t
from hak.string.filepath.py.get_t import f as get_t
from hak.test.failed.handle import f as handle_failed_test
from hak.test.passed.handle import f as handle_passed_test

excludables = set([
  './start.py',
  './gitter.py',
  './hak/data/months.py',
  './hak/data/kana.py',
  './hak/data/macbook_screen_resolutions.py',
  './hak/data/si_prefixes.py',
])

def make_Pi_t(python_filepaths, test_all, prev, last_mods):
  return (
    python_filepaths.copy()
    if test_all
    else [
      p
      for p
      in python_filepaths
      if (
        (prev[p] if p in prev else 0)
        !=
        (last_mods[p] if p in last_mods else 0)
      )
    ]
  ) or python_filepaths.copy()

def f(test_all=False, t_0=time()):
  testables = sorted([
    pyfilepath
    for pyfilepath
    in list_testables()
    if all([
      pyfilepath not in excludables,
      not pyfilepath.startswith('./data/')
    ])
  ])

  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as _: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in testables}
  save(last_mods, './last_modified.pickle')
  _A = [_[0] for _ in sort(last_mods)[::-1]]
  _B = set(make_Pi_t(testables, test_all, prev, last_mods))
  Pi_t = [a for a in _A if a in _B]
  pyfile_data = pyfiles_to_dict(Pi_t)
  max_len = 0
  for pi_index, py_filepath in enumerate(Pi_t):
    content = pyfile_data[py_filepath]
    _m = ' '.join([
      f'[{(100*(pi_index+1)/len(Pi_t)):> 7.2f} % of',
      f'{pi_index+1:3}/{len(Pi_t)} files.] Checking {py_filepath}'
    ])
    max_len = max(max_len, len(_m))
    print(f'{_m:<{max_len}}')
    
    if not has_t(content): return handle_failed_test(
      set(),
      py_filepath,
      danger(" has no ")+warn('t()')
    )
    
    if not has_f(content): return handle_failed_test(
      set(),
      py_filepath,
      danger(" has no ")+warn('f()')
    )

    if not get_t(py_filepath)(): return handle_failed_test(
      set(),
      py_filepath,
      ''
    )

  return handle_passed_test(t_0, Pi_t)
