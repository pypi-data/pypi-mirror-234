from datetime import date

from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(year: int):
  g = year % 19
  c = year / 100
  h = (c - (c // 4) - int((8 * c + 13) / 25) + 19 * g + 15) % 30
  i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
  d = int(i - ((year + (year // 4) + i + 2 - c + (c // 4)) % 7) + 28)
  m = 4 if d > 31 else 3
  if d > 31: d -= 31
  return date(year, m, d)

def t():
  if not pxyf(2022, date(2022,  4, 17), f): return pf('t_easter_2022')
  if not pxyf(2023, date(2023,  4,  9), f): return pf('t_easter_2023')
  if not pxyf(2024, date(2024,  3, 31), f): return pf('t_easter_2024')
  return 1
