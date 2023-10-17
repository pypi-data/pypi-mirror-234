from hak.number.log_2 import f as log_2
from math import ceil

w_max = 23

# hak.calculate_duration_bar_width
f = lambda t_ms: 0 if t_ms <= 0 else min(max(0, ceil(log_2(t_ms))), w_max)

t = lambda: all([
  f(-1) == 0,
  f(0) == 0,
  *[f(2**_) == _ for _ in range(24)],
  f(9000000) == 23,
])
