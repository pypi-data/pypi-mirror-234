from random import choices

def f(x):
  Σ = sum(x.values())
  _zippable = {k: x[k]/Σ for k in x}.items()
  try:
    _K, _P = zip(*_zippable)
  except ValueError as ve:
    print(f'x:         {x}')
    print(f'_zippable: {_zippable}')
    print(f've: {ve}')
    return []
  return choices(_K, weights=_P)[0]

def t():
  n = 1000
  x = {'A': 9, 'B': 1}
  z = [f(x) for _ in range(n)]
  z_freq = {_: len([i for i in z if i == _]) for _ in 'AB'}
  return all([round(z_freq['A']/n, 1)==0.9, round(z_freq['B']/n, 1)==0.1])
