from subprocess import run as sprun
from hak.directory.make import f as mkdir
from hak.directory.remove import f as rmdir

up = lambda: mkdir('../temp_git_init')
dn = lambda x: rmdir(x)

args = ['git', 'init']

f = lambda cwd: sprun(cwd=cwd, capture_output=True, args=args)

def t():
  x = up()
  z = f(x)
  dn(x)
  return all([
    z.args==args,
    z.returncode==0,
    'Initialized empty Git repository in' in z.stdout.decode('utf-8'),
    not z.stderr.decode('utf-8')
  ])
