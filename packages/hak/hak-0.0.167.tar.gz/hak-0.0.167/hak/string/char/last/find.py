f = lambda x_str, x_char: (len(x_str) - x_str[::-1].find(x_char) -1)

t = lambda: all([
  f('abcdeabcde', 'a') == 5,
  f('abcdeabcde', 'b') == 6,
  f('abcdeabcde', 'd') == 8
])
