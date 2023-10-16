from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdir
from hak.file.load import f as load
from hak.file.remove import f as remove
from hak.file.save import f as save

f = lambda filename, data: save(filename, data)

up = lambda: mkdirine('./temp')

dn = lambda dirname, filename: [remove(filename), rmdir(dirname)]

def t():
  dirname = up()
  _data = '\n'.join(["f = lambda: None", "t = lambda: False", ""])
  y = _data
  filename = f'{dirname}/foo.py'
  f(filename, _data)
  z = load(filename)
  dn(dirname, filename)
  return y == z
