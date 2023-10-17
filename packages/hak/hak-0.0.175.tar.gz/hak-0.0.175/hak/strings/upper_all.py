# f_upper_all
f = lambda x: [_.upper() for _ in x]
t = lambda: f(['ABc', 'GhI', 'jKL']) == ['ABC', 'GHI', 'JKL']
