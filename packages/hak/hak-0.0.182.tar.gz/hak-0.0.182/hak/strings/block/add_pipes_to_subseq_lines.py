from hak.pxyf import f as pxyf
from hak.strings.block.to_str import f as block_to_str

def f(x):
  recurse = False
  y = []
  y.append(x[0])
  for i in range(1, len(x)):
    y_line = ''
    for j in range(len(x[i])):
      previous = x[i-1][j]
      current = x[i][j]
      if previous == '|' and current == ' ':
        current = '|'
        recurse = True
      y_line += current
    y.append(y_line)
    if recurse: y = f(y)
  return y

def t():
  x = [
    '-----------------------------------------------------------------',
    '          A          |          cash_flow           |    date    ',
    '---------------------|------------------------------|            ',
    '        cash         | amount |   name   |   type   |            ',
    '---------------------|                              |            ',
    ' primary | secondary |                              |            '
  ]
  y = [
    '-----------------------------------------------------------------',
    '          A          |          cash_flow           |    date    ',
    '---------------------|------------------------------|            ',
    '        cash         | amount |   name   |   type   |            ',
    '---------------------|        |          |          |            ',
    ' primary | secondary |        |          |          |            '
  ]
  z = f(x)
  if y != z:
    print(block_to_str(z))
  return pxyf(x, y, f)
