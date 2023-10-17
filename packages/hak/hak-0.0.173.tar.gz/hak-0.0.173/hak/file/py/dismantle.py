from hak.file.load import f as load
from hak.string.separate_function_from_context import f as separate
from hak.directory.make import f as mkdir
from hak.directory.remove import f as rmdir
from hak.string.split_fn_name_and_text import f as split_fn_name_and_text
from hak.file.save import f as save
from hak.string.fn_name.is_ignorable import f as function_is_ignorable
from hak.string.prepend_import import f as prepend_import
from hak.dict.proposed_dismantlement.show import f as show_proposed
from hak.check_if_ok_to_proceed import f as check_if_ok_to_proceed
from hak.function.write_to_file import f as write_function_to_file
from hak.function.function import Function

def f(_pi_filename, root='.', silent=True):
  initial_content = load(_pi_filename)
  (initial_function_text, initial_other_text) = separate(initial_content)

  if not initial_function_text: return

  f_name, f_body = split_fn_name_and_text(initial_function_text)

  if function_is_ignorable(f_name): return f_name

  new_content = prepend_import(f_name, initial_other_text)
  new_function_text = 'def f'+f_body

  show_proposed(
    {
      '_pi_filename': _pi_filename,
      'initial_content': initial_content,
      'new_content': new_content,
      'initial_other_text': initial_other_text,
      'initial_function_text': initial_function_text,
      'new_function_text': new_function_text
    },
    silent
  )

  check_if_ok_to_proceed(silent=silent)
  write_function_to_file(Function(name=f_name, text=new_function_text), root)
  save(_pi_filename, new_content)

_root = '../temp_pyfile_dismantle'
_pi_filename = _root+'/foo.py'

up = lambda: [
  mkdir(_root),
  save(_pi_filename, '\n'.join([
    '# Header comment',
    '',
    'def foo(x, y, z):',
    '  return x + y + z',
    '',
    'def goo(i, j):',
    '  return i * j',
    '',
    "if __name__ == '__main__':",
    '  print(foo(goo(1, 2), 3, 4))',
    ''
  ]))
]

dn = lambda: rmdir(_root)

def t():
  up()
  original_file_content = load(_pi_filename)
  f(_pi_filename, _root, silent=True)
  extracted_file_content = load( _root+'/_foo.py')
  updated_file_content = load(_pi_filename)
  dn()
  return all([
    original_file_content != updated_file_content,
    extracted_file_content == '\n'.join([
      'def f(x, y, z):',
      '  return x + y + z',
      '',
      ''
    ]),
    updated_file_content == '\n'.join([
      'from _foo import f as foo',
      '',
      '# Header comment',
      '',
      'def goo(i, j):',
      '  return i * j',
      '',
      "if __name__ == '__main__':",
      '  print(foo(goo(1, 2), 3, 4))',
      ''
    ])
  ])
