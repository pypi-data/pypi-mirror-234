from hak.directory.make import f as mkdir
from hak.file.save import f as save
from hak.strings.filepaths.py.get import f as list_py_files
from hak.strings.pyfiles.filter_out_items import f as ignore_protected
from hak.file.py.dismantle import f as dismantle
from hak.file.load import f as load
from hak.directory.remove import f as rmdir
from hak.directory.exists import f as exists

ignorable = [f'./hak/{_}.py' for _ in [
  'hak',
  'file/load',
  'terminal',
  'refactor_recommender'
]]

f = lambda root='.': [
  dismantle(_pi_filename=_pi, root=root)
  for _pi in ignore_protected(list_py_files(root, []), ignorable)
]

_root = '../temp_pyfiles_dismantle'
K = ['foo', 'bar']
_Pi_path_original = {k: f'{_root}/{k}.py' for k in K}
_Pi_path_new = {k: f'{_root}/_{k}.py' for k in K}
_Pi_content = {k: '\n'.join([
    '# Header comment',
    '',
    f'def {k}(x, y, z):',
    '  return x + y + z',
    '',
    "if __name__ == '__main__':",
    f'  print({k}(2, 3, 4))',
    ''
  ])
  for k in K
}

def up(): return [
  mkdir(_root),
  *[save(_Pi_path_original[k], _Pi_content[k]) for k in K]
]

dn = lambda: rmdir(_root)

def t():
  up()

  _Pi_original_content = {k: load(_Pi_path_original[k]) for k in K}
  z = f(_root)
  _Pi_observed_updated = {k: load(_Pi_path_original[k]) for k in K}
  _Pi_observed_new = {k: load(_Pi_path_new[k]) for k in K}
  
  dn()

  return all([
    _Pi_original_content != _Pi_observed_updated,
    *[len(_Pi_original_content[k]) > len(_Pi_observed_updated[k]) for k in K],
    *[len(_Pi_original_content[k]) > len(_Pi_observed_new[k]) for k in K],
    *[k in _Pi_observed_updated[k] for k in K],
    *[f'_{k}' in _Pi_observed_updated[k] for k in K],
    *[k in _Pi_observed_updated[k] for k in K],
    not exists(_root)
  ])
