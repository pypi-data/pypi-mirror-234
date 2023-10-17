from hak.string.hbar.make import f as hbar
from hak.string.header.python_file.make import f as make_py_filename_header
from hak.string.make_initial_content import f as make_initial_content
from hak.string.make_function_text import f as make_function_text
from hak.string.make_new_function_text import f as make_new_function_text
from hak.string.make_content_without_function import f as make_content_wo_fn
from hak.terminal import Terminal

def f(_pi, silent=False, term=Terminal()):
  if silent: term.mode = 'test'
  term.clear()
  return term.print('\n'.join([
    hbar(),
    make_py_filename_header(_pi['_pi_filename']),
    make_initial_content(_pi['_pi_filename'], _pi['initial_content']),
    make_function_text(_pi['_pi_filename'], _pi['initial_function_text']),
    make_new_function_text(_pi['_pi_filename'], _pi['new_function_text']),
    make_content_wo_fn(_pi['_pi_filename'], _pi['initial_other_text'])
  ]))

t = lambda: f({
  '_pi_filename': 'foo.py',
  'initial_content': 'abc',
  'initial_function_text': 'def ghi(): return 0',
  'new_function_text': 'def ghi(): return 1',
  'initial_other_text': 'blergh'
}, True)=='\n'.join([
  hbar(), '\x1b[1;36mpython_file:\x1b[0;0m foo.py',
  hbar('='), '\x1b[1;36mfoo.py initial_content:\x1b[0;0m', 'abc',
  hbar(), '\x1b[1;36mfoo.py function_text:\x1b[0;0m',
  'def ghi(): return 0',
  hbar(), '\x1b[1;36mfoo.py new_function_text:\x1b[0;0m',
  'def ghi(): return 1',
  hbar(), '\x1b[1;36mfoo.py content_without_function:\x1b[0;0m',
  'blergh',
  hbar()
])
