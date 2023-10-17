# _l

f = lambda body: eval("lambda x: "+body.replace('\n', '\\n'))

t_x_squared = lambda: f("x*x")(2) == 4
t_newline_replacement = lambda: all([
  f("'\n\n' in x")('\n\n\n'), not f("'\n\n' in x")('abc')
])

t_newline_replacement_with_space = lambda: all([
  f("'\n \n' in x")('abc\n \n\nxyz'), not f("'\n \n' in x")('abc')
])

t = lambda: all([
  t_x_squared(),
  t_newline_replacement(),
  t_newline_replacement_with_space()
])
