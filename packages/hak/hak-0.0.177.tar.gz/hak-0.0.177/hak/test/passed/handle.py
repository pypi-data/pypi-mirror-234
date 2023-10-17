from os.path import exists
from time import time

from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from hak.file.pickle.save import f as save_pickle
from hak.file.remove import f as remove
from hak.string.colour.bright.green import f as success

def f(t_0, _Pi_to_test, t_now=None):
  t_now = t_now or time()
  remove('./failed.pickle')
  return {
    'result': True,
    'message': ' '.join([
      f"{success('PASS')}",
      f"{1000*(t_now-t_0):0.2f} ms.",
      f"Tested: {_Pi_to_test}"
    ])
  }

_dir = './_handle_pass'
_failed_pickle_path = f'{_dir}/failed.pickle'

def up(): mkdirine(_dir); save_pickle({}, _failed_pickle_path)

def dn(): rmdirie(_dir)

def t():
  up()
  y = {
    'result': True,
    'message': '\x1b[1;32mPASS\x1b[0;0m 1000.00 ms. Tested: []'
  }
  z = f(0, [], 1)
  _failed_pickle_exists = exists(_failed_pickle_path)
  dn()
  return all([y == z, _failed_pickle_exists])
