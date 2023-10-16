from hak.file.load import f as load
from hak.file.remove import f as remove
from hak.file.save import f as save_file
from hak.pf import f as pf
from hak.string.colour.bright.green import f as success
from hak.string.colour.bright.red import f as danger
from hak.strings.filepaths.py.testables.get import f as list_testables
from hak.terminal import Terminal

# check_final_line

def f(filepaths=None, term=None):
  term = term or Terminal()
  term.print('Checking final lines...', end='\r')
  filepaths = filepaths or list_testables()
  for pi in filepaths:
    _lines = load(pi).split('\n')
    _last_index = len(_lines)-1
    l = _lines[_last_index]
    if l != '': return pf([f'{pi}:{_last_index}', danger([l])], p=term.print)
  term.print(f"{success('PASS')} Final lines "+' '*20)
  return 1

def t_expected_false():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save_file(k, v)
  
  x = list(_test_files.keys())
  y = 0
  y_out_stream_list = [
    'Checking final lines...\r',
    "./a.pz:1\n\x1b[1;31m['xyz']\x1b[0;0m\n"
  ]
  term = Terminal(mode='test')
  z = f(x, term=term)
  
  for k in _test_files: remove(k)

  if y != z: return pf([f'x: {x}', f'y: {y}', f'z: {z}'])
  if term.output_stream_as_list != y_out_stream_list: return pf([
    'term.output_stream_as_list != y_out_stream_list',
    f'term.output_stream_as_list: {term.output_stream_as_list}',
    f'y_out_stream_list:          {y_out_stream_list}',
  ])
  return 1

def t_expected_true():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz", '']),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save_file(k, v)
  
  x = list(_test_files.keys())
  y = 1
  y_out_stream_list = [
    'Checking final lines...\r',
    '\x1b[1;32mPASS\x1b[0;0m Final lines                     \n'
  ]
  term = Terminal(mode='test')
  z = f(x, term=term)
  
  for k in _test_files: remove(k)

  if y != z: return pf([f'x: {x}', f'y: {y}', f'z: {z}'])
  if term.output_stream_as_list != y_out_stream_list: return pf([
    'term.output_stream_as_list != y_out_stream_list',
    f'term.output_stream_as_list: {term.output_stream_as_list}',
    f'y_out_stream_list:          {y_out_stream_list}',
  ])
  return 1

def t():
  if not t_expected_true(): return pf('not t_expected_true()')
  if not t_expected_false(): return pf('not t_expected_false()')
  return 1
