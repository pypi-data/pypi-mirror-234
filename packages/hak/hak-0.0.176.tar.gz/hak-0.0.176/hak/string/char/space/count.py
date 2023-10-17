from hak.string.char.count import f as count_char

f = lambda x: count_char(x, ' ')

t = lambda: all([f('a') == 0, f('a b') == 1, f('a b c') == 2])
