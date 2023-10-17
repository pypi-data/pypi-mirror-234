from hak.system.git.push_after_delay import f as push_commits_after_delay
from hak.strings.filepaths.py.get import f as list_py_files
from hak.strings.pyfiles.filter_out_items import f as filter_out_items
from hak.pyfiles.format import f as auto_format_py_filenames
from hak.pxyz import f as pxyz

def f(x, fn_a=auto_format_py_filenames, fn_b=push_commits_after_delay):
  return fn_a(x), fn_b(5)

def t():
  x = {'x': list('abc'), 'fn_a': lambda x: x, 'fn_b': lambda x: x}
  return pxyz(x, (list('abc'), 5), f(**x))

if __name__ == '__main__':
  f(
    filter_out_items(
      list_py_files(),
      [
        './haki.pyfiles.format_and_commit.py',
        # './data.py',
        # './_auto_format_one.py',
        # './src/x_contains_run_function.py',
        # './src/x_contains_test_function.py',
        # './src/data.py',
        # './src/auto_format_one.py',
      ]
    )
  )
