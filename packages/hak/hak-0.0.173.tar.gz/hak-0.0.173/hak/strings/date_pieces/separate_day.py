from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.day.is_a import f as is_day
from hak.string.month.is_a import f as is_month

def f(x):
  a, b = x
  a_m = is_month(a)
  b_m = is_month(b)
  a_d = is_day(a)
  b_d = is_day(b)

  if       a_m and     b_m and     a_d and     b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!A')
    
  elif     a_m and     b_m and     a_d and not b_d: return int(a), set([b])
  elif     a_m and     b_m and not a_d and     b_d: return int(b), set([a])
  elif     a_m and     b_m and not a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!D')
    
  elif     a_m and not b_m and     a_d and     b_d: return int(b), set([a])
  elif     a_m and not b_m and     a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!F')
    
  elif     a_m and not b_m and not a_d and     b_d: return int(b), set([a])
  elif     a_m and not b_m and not a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!H')
    
  elif not a_m and     b_m and     a_d and     b_d: return int(a), set([b])
  elif not a_m and     b_m and     a_d and not b_d: return int(a), set([b])
  elif not a_m and     b_m and not a_d and     b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!K')
    
  elif not a_m and     b_m and not a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!L')
    
  elif not a_m and not b_m and     a_d and     b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!M')
    
  elif not a_m and not b_m and     a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!N')
    
  elif not a_m and not b_m and not a_d and     b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!O')
    
  elif not a_m and not b_m and not a_d and not b_d:
    pf([
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!P')
  
  else:
    pf([
      'This branch should be impossible',
      f'x: {x}',
      f'a: {a:>3} | {a_m:>1} | {a_d:>1}',
      f'b: {b:>3} | {b_m:>1} | {b_d:>1}',
      ''
    ])
    raise NotImplementedError('!P')

def t():
  if not pxyf(set([ '19', 'Nov']), (19, set(['Nov'])), f): return pf('!t_0')
  if not pxyf(set([ '11',  '19']), (19, set([ '11'])), f): return pf('!t_1')
  if not pxyf(set([ '03',  '28']), (28, set([ '03'])), f): return pf('!t_2')
  if not pxyf(set([ '07', 'Jan']), ( 7, set(['Jan'])), f): return pf('!t_3')
  if not pxyf(set(['Jan',  '07']), ( 7, set(['Jan'])), f): return pf('!t_4')
  return 1
