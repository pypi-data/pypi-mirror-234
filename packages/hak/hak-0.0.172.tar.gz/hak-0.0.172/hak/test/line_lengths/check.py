from hak.file.load import f as load
from hak.file.remove import f as remove
from hak.file.save import f as save
from hak.pf import f as pf
from hak.string.colour.bright.green import f as success
from hak.string.colour.bright.red import f as danger
from hak.strings.filepaths.py.testables.get import f as list_testables
from hak.terminal import Terminal

# check_line_lengths

def f(filepaths=None, term=None):
  term = term or Terminal()
  term.print('Checking line lengths...', end='\r')
  filepaths = filepaths or list_testables()
  for pi in filepaths:
    ignore_line_lengths = False
    for line_index, line in enumerate(load(pi).split('\n')):
      if 'ignore_overlength_lines' in line: ignore_line_lengths = True
      if len(line) > 80 and not ignore_line_lengths: return pf([
        f'{pi}:{line_index+1}',
        danger(line)
      ], p=term.print)
  term.print(f"{success('PASS')} Line Lengths "+' '*20)
  return 1

def t_expected_true():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = 1
  y_out_stream_list = [
    'Checking line lengths...\r',
    '\x1b[1;32mPASS\x1b[0;0m Line Lengths                     \n'
  ]
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

def t_expected_false():
  w = 90
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
    './c.pz': "\n".join(["abc", "xyz", '-'*w, '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = 0
  y_out_stream_list = [
    'Checking line lengths...\r',
    './c.pz:3\n\x1b[1;31m'+'-'*w+'\x1b[0;0m\n'
  ]
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

def t():
  if not t_expected_true(): return pf('not t_expected_true()')
  if not t_expected_false(): return pf('not t_expected_false()')
  return 1
