# f_first_3_chars
f = lambda x: [_[:3] for _ in x]
t = lambda: f(['abcd', 'GhIjKL', 'mn']) == ['abc', 'GhI', 'mn']
