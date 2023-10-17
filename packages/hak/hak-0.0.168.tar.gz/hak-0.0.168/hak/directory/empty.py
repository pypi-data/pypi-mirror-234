from hak.directory.make import f as mkdir
from hak.file.save import f as save
from string import ascii_lowercase as az
from hak.directory.remove import f as rmdir
from os import listdir
from hak.file.remove import f as remove
from hak.pf import f as pf
from os.path import isfile
from os.path import exists

def f(x):
  if exists(x):
    for n in listdir(x):
      filepath = f'{x}/{n}'
      if isfile(filepath):
        remove(filepath)

up = lambda x: [mkdir(x), *[save(f'{x}/{_}.txt', _) for _ in az]]
dn = lambda x: rmdir(x)

def t():
  x = './temp'
  up(x)
  α = len(listdir(x))
  f(x)
  ω = len(listdir(x))
  result = all([α>ω, ω==0])
  dn(x)
  return result or pf([f'α: {α}', f'ω: {ω}'])
