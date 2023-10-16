from hak.string.contains.l import f as contains_lambda

def f(x):
  lines_containing_lambda = [_l for _l in x.split('\n') if contains_lambda(_l)]
  if lines_containing_lambda:
    for _l in lines_containing_lambda:
      x = x.replace(_l, '\n'+_l)
  return x

t = lambda: all([
  '\nf = lambda ' == f('f = lambda '),
  '\nf = lambda self: 0' == f('f = lambda self: 0'),
  '\nf = lambda:' == f('f = lambda:'),
  '\nt = lambda ' == f('t = lambda '),
  '\nt = lambda:' == f('t = lambda:'),
  '\nrun = lambda ' == f('run = lambda '),
  '\nrun = lambda:' == f('run = lambda:'),
  '\ntest = lambda ' == f('test = lambda '),
  '\ntest = lambda:' == f('test = lambda:'),
])
