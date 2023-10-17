from copy import deepcopy
from hak.directory.empty import f as empty_directory
from hak.directory.make import f as mkdir
from hak.directory.remove import f as rmdirie
from hak.file.load import f as load
from hak.file.save import f as save
from hak.pf import f as pf
from hak.system.git.commit.run import f as add_to_git
from hak.system.git.commit.run import t as t_add_to_git
from hak.other.pip.dist_tar.make import f as make_new_dist_tar
from hak.other.pip.dist_tar.make import t as t_make_new_dist_tar
from hak.other.pip.dist_tar.remove import t as t_remove_dist_tar
from hak.other.pip.upload import f as start_upload
from hak.other.pip.upload import t as t_start_upload
from hak.other.pip.version.get import f as get_pip_version
from hak.other.pip.version.get import t as t_get_pip_version
from hak.other.setup.cfg.update import f as update_setup_cfg
from hak.other.setup.cfg.update import t as t_update_setup_cfg
from hak.other.setup.py.update import f as update_setup_py
from hak.other.setup.py.update import t as t_update_setup_py
from subprocess import run as sprun

def f(x):
  x = deepcopy(x)
  z = {}
  z['v'] = x['v'] if 'v' in x else None
  z['root'] = x['root'] if 'root' in x else '.'
  z['cfg_path'] = f'{z["root"]}/setup.cfg'
  z['py_path'] = f'{z["root"]}/setup.py'

  z['v'] = z['v'] or get_pip_version('hak')
  z['v']['patch'] += 1

  update_setup_cfg({'v': z['v'], 'filename': z['cfg_path']})
  update_setup_py({'v': z['v'], 'filename': z['py_path']})
  empty_directory('./dist/')
  
  make_new_dist_tar(x)
  # add_to_git(cwd=_root, cap_out=True)
  if 'local_test_only' not in x: z['upload_result'] = start_upload(x)
  return z


def up():
  x = {}
  x['root'] = f"./hak_test"
  x['cfg_path'] = f"{x['root']}/setup.cfg"
  x['py_path'] = f"{x['root']}/setup.py"

  mkdir(x['root'])

  _ = sprun(
    ['git', 'clone', 'git@gitlab.com:zereiji/hak_test.git'],
    cwd=x['root'],
    capture_output=True
  )

  x['v'] = {'major': 1, 'minor': 2, 'patch': 3}

  # x['original_setup_cfg_content'] = load(x['cfg_path'])
  save(x['cfg_path'], "\n".join([
    "[metadata]",
    "name = hak",
    f"version = {x['v']['major']}.{x['v']['minor']}.{x['v']['patch']}",
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

  # x['original_setup_py_content'] = load(x['py_path'])
  save(x['py_path'], "\n".join([
    "from setuptools import setup",
    "from pathlib import Path",
    "long_description = Path('./README.md').read_text()",
    "",
    "setup(",
    "  name='hak',",
    # "  version='1.2.4',",
    f"  version='{x['v']['major']}.{x['v']['minor']}.{x['v']['patch']+1}'",
    "  license='MIT',",
    "  description='Function Test Pair Toolbox',",
    "  long_description=long_description,",
    "  long_description_content_type='text/markdown',",
    "  author='@JohnRForbes',",
    "  author_email='john.robert.forbes@gmail.com',",
    "  url='https://github.com/JohnForbes/hak',",
    "  packages=['hak'],",
    "  keywords='hak',",
    "  install_requires=[],",
    ")",
  ]))
  return x

def dn(x):
  rmdirie(x['root'])
  # save(x['cfg_path'], x['original_setup_cfg_content'])
  # save(x['py_path'], x['original_setup_py_content'])

def t():
  x = up()
  x['local_test_only'] = True
  y = {
    'v': {'major': 1, 'minor': 2, 'patch': 4},
    'cfg_path': './hak_test/setup.cfg',
    'py_path': './hak_test/setup.py',
    'upload_result': {
      'args': ['twine', 'upload', 'dist/*', '-u', 'username', '-p', 'password'],
      'returncode': 0,
      'stdout': b'Uploading distributions to',
      'stderr': b''
    },
    'root': x['root']
  }
  z = f(x)
  dn(x)

  if z is None: return pf([f"z is None", f'x: {x}', f'y: {y}', f'z: {z}'])

  if y['v'] != z['v']:
    return pf([f"y['v'] != z['v']", f'x: {x}', f'y: {y}', f'z: {z}'])
  
  for k in (set(y.keys()) | set(z.keys())):
    if k != 'upload_result':
      if not y[k] == z[k]:
        return pf([f"y[{k}] == z[{k}]", f'x: {x}', f'y: {y}', f'z: {z}'])
  
  if not 'local_test_only':
    if not (
      len(y['upload_result']['args']) ==
      len(z['upload_result']['args']) ==
      7
    ):
      return pf([
        ' == '.join([
          "not (len(y['upload_result']['args'])",
          "len(z['upload_result']['args'])",
          "7)"
        ]),
        f"y['upload_result']['args']: {y['upload_result']['args']}",
        f"z['upload_result']['args']: {z['upload_result']['args']}"
      ])

    if not (
      y['upload_result']['args'][0] ==
      z['upload_result']['args'][0] ==
      'twine'
    ):
      return pf(' == '.join([
        "not (y['upload_result']['args'][0]",
        "z['upload_result']['args'][0]",
        "'twine')"
      ]))

    if not (
      y['upload_result']['args'][1] ==
      z['upload_result']['args'][1] ==
      'upload'
    ):
      return pf(' == '.join([
        "not (y['upload_result']['args'][1]",
        "z['upload_result']['args'][1]",
        "'upload')"
      ]))

    if not (
      y['upload_result']['args'][2] ==
      z['upload_result']['args'][2] ==
      'dist/*'
    ):
      return pf(' == '.join([
        "not (y['upload_result']['args'][2]",
        "z['upload_result']['args'][2]",
        "'dist/*')"
      ]))

    if not (
      z['upload_result']['args'][4] ==
      load('username.secret').split('\n')[0]
    ):
      return pf(' == '.join([
        "not (z['upload_result']['args'][4]",
        "load('username.secret').split('\n')[0])"
      ]))

    if not (
      z['upload_result']['args'][6] ==
      load('password.secret').split('\n')[0]
    ):
      return pf(' == '.join([
        "not (z['upload_result']['args'][6]",
        "load('password.secret').split('\n')[0])"
      ]))

    if not (
      y['upload_result']['returncode'] ==
      z['upload_result']['returncode'] ==
      0
    ):
      return pf(' == '.join([
        "not y['upload_result']['returncode']",
        "z['upload_result']['returncode']",
        "0"
      ]))

    if not (
      y['upload_result']['stderr'] ==
      z['upload_result']['stderr'] ==
      b''
    ):
      return pf(' == '.join(' == '.join(
        "not y['upload_result']['stderr']",
        "z['upload_result']['stderr']",
        "b''"
      )))

    if y['upload_result']['stdout'] not in z['upload_result']['stdout']:
      return pf([
        "y['upload_result']['stdout'] not in z['upload_result']['stdout']",
        f"y['upload_result']['stdout']: {y['upload_result']['stdout']}",
        f"z['upload_result']['stdout']: {z['upload_result']['stdout']}"
      ])

  if not t_get_pip_version():
    return pf([f"t_get_pip_version()", f'x: {x}', f'y: {y}', f'z: {z}'])

  if not t_update_setup_cfg():
    return pf([f"t_update_setup_cfg()", f'x: {x}', f'y: {y}', f'z: {z}'])

  if not t_update_setup_py():
    return pf([f"t_update_setup_py()", f'x: {x}', f'y: {y}', f'z: {z}'])

  if not t_remove_dist_tar():
    return pf([f"t_remove_dist_tar()", f'x: {x}', f'y: {y}', f'z: {z}'])

  if not t_make_new_dist_tar():
    print(f"t_make_new_dist_tar()")
    print(f'x: {x}')
    for k in (set(y.keys()) | set(z.keys())):
      if y[k] != z[k]:
        print('\n'.join([f'y[{k}]: {y[{k}]}', f'z[{k}]: {z[{k}]}', '']))
    return 0

  if not t_add_to_git():
    return pf([f"t_add_to_git()", f'x: {x}', f'y: {y}', f'z: {z}'])

  if not t_start_upload():
    return pf([f"t_start_upload()", f'x: {x}', f'y: {y}', f'z: {z}'])

  return 1
