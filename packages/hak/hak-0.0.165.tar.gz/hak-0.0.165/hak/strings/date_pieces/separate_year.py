from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.string.year.is_a import f as is_year

# src.set.date_pieces.separate_year
# separate_year_from_bag
def f(x):
  year = None
  new_bag = set([])
  for item in x:
    if is_year(item):
      year = int(item)
    else:
      new_bag.add(item)
  return year, new_bag

t_0 = lambda: pxyf(set([  '19', 'Nov', '2021']), (2021, set(['19', 'Nov'])), f)
t_1 = lambda: pxyf(set(['2021',  '11',   '19']), (2021, set(['11',  '19'])), f)
t_2 = lambda: pxyf(set(['2022',  '03',   '28']), (2022, set(['03',  '28'])), f)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  return 1
