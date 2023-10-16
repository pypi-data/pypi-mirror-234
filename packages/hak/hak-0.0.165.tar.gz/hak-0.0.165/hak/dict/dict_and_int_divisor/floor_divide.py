from hak.pxyf import f as pxyf

f = lambda x: {k: v//x['divisor'] for (k, v) in x['dict'].items()}
t = lambda: pxyf({'dict': {'a': 2, 'b': 4}, 'divisor': 2}, {'a': 1, 'b': 2}, f)
