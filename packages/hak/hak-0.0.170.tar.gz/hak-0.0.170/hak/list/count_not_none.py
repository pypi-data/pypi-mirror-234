# count_not_none
f = lambda x: sum([1 for _ in x if _ is not None])
t = lambda: f([1, 2.3, 4 + 5j, '6', None, None, False]) == 5
