from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdir
from hak.directory.exists import f as directory_exists

f = lambda directories: all([directory_exists(d) for d in directories])

root = './temp'
directories = [f'{root}/{directory}' for directory in ['abc', 'ghi', 'jkl']]
up = lambda: [mkdirine(d) for d in [root, *directories]]
dn = lambda: rmdir(root)

def t():
  up()
  expected_pass = f(directories)

  rmdir(root)
  expected_fail = f(directories)

  result = all([expected_pass, not expected_fail])

  dn()
  return result
