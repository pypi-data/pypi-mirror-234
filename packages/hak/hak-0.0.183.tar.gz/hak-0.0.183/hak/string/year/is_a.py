from hak.pxyf import f as pxyf

# src.string.year.is_a
# is_year
f = lambda x: len(x) == 4 and x.isdecimal()
t = lambda: pxyf('2022', 1, f) 
