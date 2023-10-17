from hak.dict.is_a import f as is_dict
from hak.pf import f as pf
from hak.pxyz import f as pxyz

# misc.dict.keypaths.leaf.get
# make_b
def f(record, path_so_far, keypaths):
  for k in record:
    keypaths |= (
      f(record[k], path_so_far+[k], keypaths)
      if is_dict(record[k]) else
      set([tuple(path_so_far+[k])])
    )
  return keypaths

def t_a():
  x = {
    'record': {
      'Name': 'Alice',
      'Info': {
        'Age': 28,
        'Country': 'USA',
        'Appearance': {'Eye Colour': 'Green', 'Height': 1.85}
      }
    },
    'path_so_far': [],
    'keypaths': set()
  }
  return pxyz(
    x,
    set([
      ('Name',),
      ('Info', 'Age'),
      ('Info', 'Country'),
      ('Info', 'Appearance', 'Eye Colour'),
      ('Info', 'Appearance', 'Height')
    ]),
    f(**x),
    new_line=1
  )

def t():
  if not t_a(): return pf('!t_a')
  return 1
