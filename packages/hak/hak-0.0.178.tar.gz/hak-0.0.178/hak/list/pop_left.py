from hak.pxyf import f as pxyf

f = lambda x: (x[1:], x[:1][0])
t = lambda: pxyf(['a', 'b', 'c'], (['b', 'c'], 'a'), f)
