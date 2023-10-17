# f_lower_all
f = lambda x: [_.lower() for _ in x]
t = lambda: f(['ABc', 'GhI', 'jKL']) == ['abc', 'ghi', 'jkl']
