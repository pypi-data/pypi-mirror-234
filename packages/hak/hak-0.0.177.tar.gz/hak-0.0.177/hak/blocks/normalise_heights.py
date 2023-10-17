from typing import List

from hak.block.is_a import f as is_block
from hak.blocks.get_max_height import f as get_h_max
from hak.blocks.get_max_height import f as get_max_block_height
from hak.classes.block import Block
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  return (_f_blocks if is_block(x[0]) else _f_lists_of_strings)(x)

def _f_lists_of_strings(blocks):
  max_block_height = get_max_block_height(blocks)
  for b in blocks:
    while len(b) < max_block_height:
      b.append(' '*len(b[0]))
  return blocks

def _f_blocks(blocks: List[Block]) -> Block:
  h_max = get_h_max(blocks)
  for b in blocks:
    while b.h < h_max:
      b.append_line('')
  return blocks

def t_blocks():
  x = [
    Block([' james ']),
    Block([
      '    john    ',
      '------------',
      ' rei | zenn '
    ])
  ]
  y = [
    Block([
      ' james ',
      '       ',
      '       '
    ]),
    Block([
      '    john    ',
      '------------',
      ' rei | zenn '
    ])
  ]
  return pxyf(x, y, f)

def t_strings():
  x = [
    [     ' james '],
    ['    john    ', '------------', ' rei | zenn ']
  ]
  y   = [
    [     ' james ',      '       ',      '       '],
    ['    john    ', '------------', ' rei | zenn ']
  ]
  return pxyf(x, y, f)

def t():
  if not t_blocks(): return pf('!t_blocks')
  if not t_strings(): return pf('!t_strings')
  return 1
