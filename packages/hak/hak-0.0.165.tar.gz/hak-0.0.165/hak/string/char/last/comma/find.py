from hak.string.find_last_char import f as find_last_char
from hak.pxyf import f as pxyf

f = lambda x: find_last_char(x, ',')
t = lambda: pxyf('a,b,c,de', 5, f)
