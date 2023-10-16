from hak.directory.remove import f as rmdir
from os.path import exists
from subprocess import run as sprun
from hak.file.zip.extract import f as extract
from time import sleep as time_sleep
from hak.fake.sleep import f as fake_sleep

_dir_name = '../temp'
base = './hak/system/git/commit'

codes = {'A ': 'Added', 'D ': 'Removed', 'R ': 'Renamed', 'M ': 'Modified'}

def f(do_pull=True, cwd='.', do_push=True, cap_out=True, sleep=time_sleep):
  if do_pull:
    sprun(['git', 'pull'], cwd=cwd, capture_output=cap_out)
    sleep(0.05)

  sprun(['git', 'add', '-A'], cwd=cwd, capture_output=cap_out)
  sleep(0.05)

  short_git_status_output = sprun(
    ['git', 'status', '--short'],
    capture_output=cap_out,
    cwd=cwd
  )

  short_git_status_lines = [
    _
    for _
    in short_git_status_output.stdout.decode('utf-8').split('\n')
    if len(_)>0
  ]

  message = '  '.join([
    f'{codes[l]} {r}.'
    for (l, r)
    in [(_[:2], _[3:]) for _ in short_git_status_lines]
  ])

  sprun(['git', 'commit', '-m', message], capture_output=cap_out, cwd=cwd)
  sleep(0.05)
  
  if do_push:
    sprun(['git', 'push'], cwd=cwd, capture_output=False)
    sleep(0.05)

setup_added = lambda: extract(f'{base}/added_file_pre_commit.zip', '..')
setup_deleted = lambda: extract(f'{base}/deleted_file_pre_commit.zip', '..')
setup_renamed = lambda: extract(f'{base}/renamed_file_pre_commit.zip', '..')
setup_modified = lambda: extract(f'{base}/modified_file_pre_commit.zip', '..')
dn = lambda: rmdir(_dir_name)

observe = lambda: sprun(
  ['git', 'log', '--pretty=oneline'],
  capture_output=True,
  cwd=_dir_name
).stdout.decode('utf-8').split('\n')[0][41:]

def t_added():
  setup_added()
  f(do_pull=False, do_push=False, sleep=fake_sleep, cwd=_dir_name)
  y = 'Added foo.py.'
  z = observe()
  result = y == z
  dn()
  return result

def t_deleted():
  setup_deleted()
  f(do_pull=False, do_push=False, sleep=fake_sleep, cwd=_dir_name)
  y = 'Removed README.md.'
  z = observe()
  result = y == z
  dn()
  return result

def t_renamed():
  setup_renamed()
  f(do_pull=False, do_push=False, sleep=fake_sleep, cwd=_dir_name)
  y = 'Renamed README.md -> renamed_readme.md.'
  z = observe()
  result = y == z
  dn()
  return result

def t_modified():
  setup_modified()
  f(do_pull=False, do_push=False, sleep=fake_sleep, cwd=_dir_name)
  y = 'Modified README.md.'
  z = observe()
  result = y == z
  dn()
  return result

def t():
  if exists(_dir_name): dn()
  return all([t_added(), t_deleted(), t_renamed(), t_modified()])
