from hak.pxyf import f as pxyf

f = lambda x: [_ for _ in x if _]
t = lambda: pxyf([1, 0, 2, 0, 3], [1, 2, 3], f)
