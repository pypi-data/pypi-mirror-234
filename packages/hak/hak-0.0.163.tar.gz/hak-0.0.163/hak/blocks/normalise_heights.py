from hak.blocks.get_max_height import f as get_max_block_height
from hak.pxyf import f as pxyf

def f(x):
  max_block_height = get_max_block_height(x)
  for block in x:
    while len(block) < max_block_height:
      block.append(' '*len(block[0]))
  return x

def t():
  x = [
    [     ' james '],
    ['    john    ', '------------', ' rei | zenn ']
  ]
  y   = [
    [     ' james ',      '       ',      '       '],
    ['    john    ', '------------', ' rei | zenn ']
  ]
  return pxyf(x, y, f)
