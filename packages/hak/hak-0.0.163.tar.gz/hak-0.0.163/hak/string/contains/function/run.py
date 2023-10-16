Γ = [
  'def f(',
  'def f():',
  'def f(x):',
  'def f(a, b):',
  'f = lambda a, b:',
  'f = lambda x:',
  'f = lambda:',
  'f = lambda',
]

f = lambda x: any([_l.startswith(γ) for γ in Γ for _l in x.split('\n')])

t = lambda: all([
  f("f = lambda x:"),
  not f("t = lambda: 0"),
  f("f = lambda x: x\nt = lambda: 0"),
  not f(""),
])
