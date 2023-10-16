from hak.pf import f as pf

f = lambda u, v, y, z: y==z or pf([f'u: {u}', f'v: {v}', f'y: {y}', f'z: {z}'])

t = lambda: True
