from hak.pxyf import f as pxyf

# vstack
def f(x):
  result = []
  w = len(x[0][0])
  for x_i in x[:-1]:
    result += x_i + ['-'*w]
  result += x[-1]
  return result

def t():
  u = [
    "---------------",
    "          Info ",
  ]
  v = [
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ]
  x = [u, v]
  y = [
    "---------------",
    "          Info ",
    "---------------",
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ]
  return pxyf(x, y, f, new_line=1)
