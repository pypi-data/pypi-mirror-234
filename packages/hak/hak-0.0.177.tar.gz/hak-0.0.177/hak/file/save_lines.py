from os.path import exists
from os import remove
from os import mkdir
from hak.nop import f as nopx
from os import rmdir
from hak.pf import f as pf

def f(filepath, lines):
  with open(filepath, 'w') as _file: _file.writelines(lines)
  return lines

_filename = './_/temp.txt'
up = lambda: (mkdir if not exists('_') else nopx)('_')

def dn():
  if exists(_filename): remove(_filename)
  rmdir('./_')

def t():
  up()
  x = ['apple\n', 'banana\n', 'carrot\n']
  z = f(_filename, x)
  if not exists(_filename): dn(); return pf(f'{_filename} not created')
  with open(_filename, 'r') as _file: lines = _file.readlines()
  if lines != x: dn(); return pf(f'{lines} != {x}')
  if z != x: dn(); return pf(f'{z} != {x}')
  dn()
  return 1
