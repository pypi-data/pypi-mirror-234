from hak.pxyf import f as pxyf

f = lambda x: [k for k in x['names'] if k not in set(x['hidden'])]
t = lambda: pxyf({'hidden': list('ace'), 'names': list('abcde')}, list('bd'), f)
