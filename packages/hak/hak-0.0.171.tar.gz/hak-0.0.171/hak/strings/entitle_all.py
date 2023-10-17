# f_title_all
f = lambda x: [_.title() for _ in x]
t = lambda: f(['abc', 'ghi', 'jkl']) == ['Abc', 'Ghi', 'Jkl']
