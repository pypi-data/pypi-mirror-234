def f(content):
  lines = content.split('\n')
  lines_containing_import = [
    l for l in lines
    if any([
      all(['import' in l, l.startswith('from')]),
      all(['import' in l, l.startswith('import')])
    ])
  ]
  if lines_containing_import:
    final_line = lines_containing_import[-1]
    return content.replace(final_line, f'{final_line}\n')
  return content

def t():
  y_0 = 'from hak.foo import run\n\nxyz'
  z_0 = f('from hak.foo import run\nxyz')
  y_1 = 'abc\nxyz'
  z_1 = f('abc\nxyz')
  y_2 = 'abc\n\nxyz'
  z_2 = f('abc\n\nxyz')
  return all([y_0 == z_0, y_1 == z_1, y_2 == z_2])
