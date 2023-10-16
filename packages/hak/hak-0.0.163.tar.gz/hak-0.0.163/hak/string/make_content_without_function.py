from hak.string.colour.info import f as info
from hak.string.hbar.make import f as hbar

f = lambda _pi_filename, content_without_function: '\n'.join([
  info(f'{_pi_filename} content_without_function:'),
  content_without_function,
  hbar()
])

t = lambda: (
  '\x1b[1;36ma.py content_without_function:\x1b[0;0m\nfooboo\n'+'-'*80
  ==
  f('a.py', 'fooboo')
)
