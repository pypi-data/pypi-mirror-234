from hak.dict.is_a import f as is_dict
from hak.list.is_a import f as is_list
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  if not is_dict(x): return 0
  if 'header' not in x: return 0
  if 'unit'   not in x: return 0
  if 'values' not in x: return 0
  if not is_list(x['values']): return 0
  return 1

t_true = lambda: pxyf({
  'header': 'apples',
  'unit': '$/apple',
  'values': [0.25, 0.75]
}, 1, f)

def t():
  if not t_true(): return pf('!t_true')
  if not pxyf(None, 0, f): return pf('!t_false')
  return 1
