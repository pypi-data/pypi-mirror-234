from hak.directory.remove import f as remove_dir
from hak.file.py.is_a import f as is_py
from hak.file.save import f as save
from hak.directory.filepaths.get import f as list_filepaths

from os import mkdir
from os import remove
from os.path import exists

# from hak.nop import f as nopx
nopx = lambda x=None: None # DELETE LINE

f = lambda root, filepaths=[]: list_filepaths(root, filepaths, is_py)

dir_a = './_list_pyfilepaths'
dir_b = f'{dir_a}/_'
temp_files_and_content = [
  (f'{dir_a}/foo.py', 'foo'), (f'{dir_a}/xyz.txt', 'xyz'),
  (f'{dir_b}/abc.txt', 'abc'), (f'{dir_b}/bar.py', 'bar'),
]

def up():
  [(nopx if exists(δ) else mkdir)(δ) for δ in [dir_a, dir_b]]
  [save(filename, content) for (filename, content) in temp_files_and_content]

def dn():
  [remove(filename) for (filename, _) in temp_files_and_content]
  [remove_dir(d) for d in [dir_b, dir_a]]

def t():
  up()
  result = set([f'{dir_b}/bar.py', f'{dir_a}/foo.py']) == set(f(dir_a, []))
  dn()
  return result
