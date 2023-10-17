from hak.pf import f as pf
from hak.pxyf import f as pxyf

# cell_val_widths_to_aggregate_width
f = lambda x: sum(x)+(len(x)-1)*len(' | ')

t_6 = lambda: pxyf(
  [6], # | 123456 |
  6,   # | 123456 |
  f
)

t_7_8 = lambda: pxyf(
  [7, 8], # | 1234567 | 12345678 |
  18,     # | 123456789012345678 |
  f
)

t_8_9_10 = lambda: pxyf(
  [8, 9, 10], # | 12345678 | 123456789 | 1234567890 |
  33,         # | 123456789012345678901234567890123 |
  f
)

t_3_10_6_7 = lambda: pxyf([3, 10, 6, 7], 35, f)

def t():
  if not t_6():        return pf('!t_6')
  if not t_7_8():      return pf('!t_7_8')
  if not t_8_9_10():   return pf('!t_8_9_10')
  if not t_3_10_6_7(): return pf('!t_3_10_6_7')
  return 1
