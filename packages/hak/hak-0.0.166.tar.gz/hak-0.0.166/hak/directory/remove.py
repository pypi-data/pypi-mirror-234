from os import listdir
from os import mkdir
from os import remove
from os import rmdir
from os.path import exists
from os.path import isdir

from hak.nop import f as nop
from hak.file.save import f as save

def f(directory, filepaths=[]):
  if not exists(directory): return
  for item in listdir(directory):
    _pi = directory+'/'+item
    f(_pi, filepaths) if isdir(_pi) else remove(_pi)
  rmdir(directory)
  return directory

temp_dir = './temp_directory_remove'
temp_files_and_content = [
  (f'{temp_dir}/foo.py', 'f = lambda: None\nt = lambda: f() is None'),
  (f'{temp_dir}/xyz.txt', 'xyz'),
]

def up():
  (mkdir if not exists(temp_dir) else nop)(temp_dir)
  [save(filename, content) for (filename, content) in temp_files_and_content]

def t(): up(); f(temp_dir); return 0 == exists(temp_dir)

