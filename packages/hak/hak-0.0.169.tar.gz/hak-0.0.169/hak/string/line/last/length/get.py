from hak.pxyz import f as pxyz

f = lambda x: len(x.split('\n')[-1])

def t():
  x = "abc\ndefg\nhijklm"
  y = 6
  z = f(x)
  return pxyz([x], [y], [z])
