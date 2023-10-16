from hak.file.load import f as load
from hak.file.save import f as save
from hak.strings.patch_setup_py import f as increment_patch_in_setup_py
from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from hak.pf import f as pf
from copy import deepcopy

def f(x):
  x = deepcopy(x)
  filename = x['filename'] if 'filename' in x else 'setup.py'
  lines = load(filename).split('\n')
  new_lines = increment_patch_in_setup_py(x['v'], lines)
  save(filename, "\n".join(new_lines))
  return None

temp_dir_path = temp_dir_path = './_setup_py_update'
temp_file_path = f'{temp_dir_path}/setup.py'

def up():
  mkdirine(temp_dir_path)
  save(temp_file_path, "\n".join([
    "from setuptools import setup",
    "from pathlib import Path",
    "long_description = Path('./README.md').read_text()",
    "",
    "setup(",
    "  name='hak',",
    "  version='1.2.3',",
    "  license='MIT',",
    "  description='Function Test Pair Toolbox',",
    "  long_description=long_description,",
    '  long_description_content_type="text/markdown",',
    "  author='@JohnRForbes',",
    "  author_email='john.robert.forbes@gmail.com',",
    "  url='https://github.com/JohnForbes/hak',",
    "  packages=['hak'],",
    "  keywords='hak',",
    "  install_requires=[],",
    ")",
  ]))

dn = lambda: rmdirie(temp_dir_path)

def t():
  x = {'v': {'major': 4, 'minor': 5, 'patch': 6}, 'filename': temp_file_path}
  y = "version='4.5.6',"
  up()
  f(x)
  z = [_ for _ in load(temp_file_path).split('\n') if 'version' in _][0]
  dn()
  return y in z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
