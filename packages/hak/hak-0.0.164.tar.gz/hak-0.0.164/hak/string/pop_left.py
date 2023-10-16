from hak.pxyf import f as pxyf

f = lambda x: (x[1:], x[:1])
t = lambda: pxyf('abcd', ('bcd', 'a'), f)
