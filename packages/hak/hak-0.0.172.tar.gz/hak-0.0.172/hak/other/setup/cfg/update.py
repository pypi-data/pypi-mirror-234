from hak.file.load import f as load
from hak.file.save import f as save
from hak.strings.patch_setup_cfg import f as increment_patch_in_setup_cfg
from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from copy import deepcopy

def f(x):
  x = deepcopy(x)
  v = x['v']
  filename = x['filename'] if 'filename' in x else 'setup.cfg'
  lines = load(filename).split('\n')
  new_lines = increment_patch_in_setup_cfg(v, lines)
  save(filename, "\n".join(new_lines))
  return None

temp_dir_path = temp_dir_path = './_setup_cfg_update'
temp_file_path = f'{temp_dir_path}/setup.cfg'

def up():
  mkdirine(temp_dir_path)
  save(temp_file_path, "\n".join([
    "[metadata]",
    "name = hak",
    "version = 1.2.3",
    "author = John Forbes",
    "author_email = john.robert.forbes@gmail.com",
    "description = Function Test Pair Toolbox",
    "long_description = file: README.md",
    "long_description_content_type = text/markdown",
    "url = https://github.com/JohnForbes/hak",
    "license_files=LICENSE",
    "classifiers = ",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    "",
    "[options]",
    "packages = find:",
    "python_requires = >=3.7",
    "include_package_data = True",
  ]))

dn = lambda: rmdirie(temp_dir_path)

def t():
  up()
  x = {'v': {'major': 4, 'minor': 5, 'patch': 6}, 'filename': temp_file_path}
  f(x)
  z = load(temp_file_path)
  dn()
  return "version = 4.5.6" in z
