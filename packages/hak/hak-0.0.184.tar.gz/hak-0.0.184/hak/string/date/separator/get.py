from hak.pf import f as pf
from hak.pxyf import f as pxyf
from string import digits

# src.string.date.separator.get
def f(x):
  d = {char: 0 for char in x if char not in digits}
  for char in x:
    if char not in digits:
      d[char] += 1
  
  for k in d:
    if d[k] == 2:
      return k

def t():
  if not pxyf( '2022-11-11', '-', f): return pf('!t_0')
  if not pxyf( '28/03/2022', '/', f): return pf('!t_1')
  if not pxyf( '2022 01 31', ' ', f): return pf('!t_2')
  if not pxyf('19 Nov 2021', ' ', f): return pf('!t_3')
  if not pxyf( '2022-05-06', '-', f): return pf('!t_4')
  return 1
