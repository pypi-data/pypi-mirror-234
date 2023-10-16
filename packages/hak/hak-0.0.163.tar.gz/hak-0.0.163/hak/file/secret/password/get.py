from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from hak.file.save import f as save
from hak.string.password.has_chars_from_3_sets import f as has_ch_from_3

filename = 'password.secret'

def f(root='.'):
  with open(f'{root}/{filename}', 'r') as φ: return φ.readlines()[0]

_root = '../temp_secret_password'
_filepath = f'{_root}/{filename}'
_content = 'abc123!@#JKLmno'
up = lambda: [mkdirine(_root), save(_filepath, _content)]
dn = lambda: rmdirie(_root)

def t():
  up()
  z = f(_root)
  result_has_characters_from_3_distinct_sets = has_ch_from_3(z)
  dn()
  return all([result_has_characters_from_3_distinct_sets, z == _content])
