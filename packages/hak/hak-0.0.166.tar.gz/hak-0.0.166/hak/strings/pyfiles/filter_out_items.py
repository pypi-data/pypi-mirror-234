from hak.pf import f as pf
from hak.pxyz import f as pxyz

f = lambda pyfiles, items: [p for p in pyfiles if p not in items]

def t_a():
  x = {'pyfiles': [], 'items': []}
  return pxyz(x, [], f(**x))

def t_b():
  x = {
    'pyfiles': ['./a.py', './b.py'],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t_c():
  x = {
    'pyfiles': ['./a.py', './hak/hak.py', './b.py'],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t_d():
  x = {
    'pyfiles': ['./a.py', './hak/get_file_lines.py', './b.py'],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t_e():
  x = {
    'pyfiles': ['./a.py', './hak/terminal.py', './b.py'],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t_f():
  x = {
    'pyfiles': [
      './a.py',
      './hak/refactor_recommender.py',
      './b.py'
    ],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t_g():
  x = {
    'pyfiles': [
      './a.py',
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
      './b.py'
    ],
    'items': [
      './hak/hak.py',
      './hak/get_file_lines.py',
      './hak/terminal.py',
      './hak/refactor_recommender.py',
    ]
  }
  return pxyz(x, ['./a.py', './b.py'], f(**x))

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  if not t_g(): return pf('!t_g')
  return 1
