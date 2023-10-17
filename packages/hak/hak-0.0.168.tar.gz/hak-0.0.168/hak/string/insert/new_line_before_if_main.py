f = lambda x: x.replace("\nif __name__ == '__ma", "\n\nif __name__ == '__ma")

def t():
  y_0 = "\n\nif __name__ == '__main__':"
  z_0 = f("\nif __name__ == '__main__':")
  y_1 = 'abc\nxyz'
  z_1 = f('abc\nxyz')
  return all([y_0 == z_0, y_1 == z_1])
