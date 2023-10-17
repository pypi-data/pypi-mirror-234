from hak.pf import f as pf

f = lambda if_true, condition, if_false: if_true if condition else if_false

def t():
  if not f('a', 0, 'b') == 'b': return pf('t_0')
  if not f('a', 1, 'b') == 'a': return pf('t_1')
  return 1
