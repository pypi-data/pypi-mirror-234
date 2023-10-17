from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.colour.bright.blue    import f as bb
from hak.string.colour.bright.cyan    import f as bc
from hak.string.colour.bright.green   import f as bg
from hak.string.colour.bright.magenta import f as bm
from hak.string.colour.bright.red     import f as br
from hak.string.colour.bright.white   import f as bw
from hak.string.colour.bright.yellow  import f as by
from hak.string.colour.dark.blue      import f as db
from hak.string.colour.dark.cyan      import f as dc
from hak.string.colour.dark.green     import f as dg
from hak.string.colour.dark.magenta   import f as dm
from hak.string.colour.dark.red       import f as dr
from hak.string.colour.dark.white     import f as dw
from hak.string.colour.dark.yellow    import f as dy

# src.string.decolour
def f(x):
  for _ in [
    '\x1b[0;0m',
    *[f'\x1b[{_a};3{_b}m' for _b in range(1, 8) for _a in range(0, 2)],
  ]:
    x = x.replace(_, '')
  return x

def t():
  if not pxyf(bb('abc'), 'abc', f, show_as_lists=1): return pf('!t_bb')
  if not pxyf(bc('abc'), 'abc', f, show_as_lists=1): return pf('!t_bc')
  if not pxyf(bg('abc'), 'abc', f, show_as_lists=1): return pf('!t_bg')
  if not pxyf(bm('abc'), 'abc', f, show_as_lists=1): return pf('!t_bm')
  if not pxyf(br('abc'), 'abc', f, show_as_lists=1): return pf('!t_br')
  if not pxyf(bw('abc'), 'abc', f, show_as_lists=1): return pf('!t_bw')
  if not pxyf(by('abc'), 'abc', f, show_as_lists=1): return pf('!t_by')
  if not pxyf(db('abc'), 'abc', f, show_as_lists=1): return pf('!t_db')
  if not pxyf(dc('abc'), 'abc', f, show_as_lists=1): return pf('!t_dc')
  if not pxyf(dg('abc'), 'abc', f, show_as_lists=1): return pf('!t_dg')
  if not pxyf(dm('abc'), 'abc', f, show_as_lists=1): return pf('!t_dm')
  if not pxyf(dr('abc'), 'abc', f, show_as_lists=1): return pf('!t_dr')
  if not pxyf(dw('abc'), 'abc', f, show_as_lists=1): return pf('!t_dw')
  if not pxyf(dy('abc'), 'abc', f, show_as_lists=1): return pf('!t_dy')
  return 1

if __name__ == '__main__': print(t())
