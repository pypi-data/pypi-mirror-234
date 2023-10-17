from hak.pxyf import f as pxyf
from hak.pf import f as pf

s = [
  '\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074',
  '\u2075', '\u2076', '\u2077', '\u2078', '\u2079',
]

def _f_side(x):
  z = ''
  for k in sorted(x):
    z += f'{k}' if len(k) > 1 else f'{k}'
    if x[k] == 1: return z
    z += ''.join([s[int(j)] for j in str(x[k])])
  return z

def f(x):
  l = _f_side({k: x[k] for k in x if x[k] > 0})
  r = _f_side({k: -x[k] for k in x if x[k] < 0})
  if r: return (l or '1')+'/'+r
  return l

t_m_1 = lambda: pxyf({'m': 1}, 'm', f)
t_m_2 = lambda: pxyf({'m': 2}, 'm\u00B2', f)
t_m_10 = lambda: pxyf({'m': 10}, 'm\u00B9\u2070', f)
t_m_20 = lambda: pxyf({'m': 20}, 'm\u00B2\u2070', f)
t_m_neg_1 = lambda: pxyf({'m': -1}, '1/m', f)
t_dollar_per_square_metre = lambda: pxyf({'$': 1, 'm': -2}, '$/m\u00B2', f)
t_m_3 = lambda: pxyf({'m': 3}, 'm\u00B3', f)
t_USD_per_AUD = lambda: pxyf({'USD': 1, 'AUD': -1}, 'USD/AUD', f)
t_USD_2_per_AUD = lambda: pxyf({'USD': 2, 'AUD': -1}, 'USD\u00B2/AUD', f)

def t():
  if not t_m_1(): return pf('!t_m_1')
  if not t_m_2(): return pf('!t_m_2')
  if not t_m_10(): return pf('!t_m_10')
  if not t_m_20(): return pf('!t_m_20')
  if not t_m_neg_1(): return pf('!t_m_neg_1')
  if not t_dollar_per_square_metre(): return pf('!t_dollar_per_square_metre')
  if not t_m_3(): return pf('!t_m_3')
  if not t_USD_per_AUD(): return pf('!t_USD_per_AUD')
  if not t_USD_2_per_AUD(): return pf('!t_USD_2_per_AUD')
  return 1
