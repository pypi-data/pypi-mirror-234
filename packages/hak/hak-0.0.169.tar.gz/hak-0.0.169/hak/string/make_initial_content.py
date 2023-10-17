from hak.string.colour.info import f as info
from hak.string.hbar.make import f as hbar

f = lambda _pi_filename, initial_content: '\n'.join([
  info(f'{_pi_filename} initial_content:'),
  initial_content,
  hbar()
])

k = 'abc\ndef\nghi\njkl'
n = 'abc.py'

t = lambda: f'\x1b[1;36m{n} initial_content:\x1b[0;0m\n{k}\n'+'-'*80 == f(n, k)
