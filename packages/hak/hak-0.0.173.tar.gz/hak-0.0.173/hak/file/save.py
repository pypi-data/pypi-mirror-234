from os.path import exists
from os import remove
from os import mkdir
from os import rmdir

from hak.pf import f as pf

# from hak.nop import f as nop
nop = lambda x=None: None # DELETE LINE

def f(filepath, content):
  with open(filepath, 'w') as φ:
    φ.write(content)
    return content

_root = './temp_save_string'
_filepath = f'{_root}/temp.txt'

up = lambda: (mkdir if not exists(_root) else nop)(_root)

def dn():
  if exists(_filepath): remove(_filepath)
  rmdir(_root)

def t():
  up()

  x_content = 'apple'
  result = f(_filepath, x_content)

  if not exists(_filepath):
    dn()
    return pf(f'{_filepath} file was not created by file.write.run()')

  with open(_filepath, 'r') as _file:
    file_content = _file.read()

  if file_content != x_content:
    dn()
    return pf(f'{file_content} != {x_content}')

  if result != x_content:
    dn()
    return pf(f'{result} != {x_content}')

  dn()
  return 1
