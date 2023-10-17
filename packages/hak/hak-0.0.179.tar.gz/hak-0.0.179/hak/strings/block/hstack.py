from typing import List

from hak.blocks.normalise_heights import f as normalise_heights
from hak.classes.block import Block
from hak.pf import f as pf
from hak.pxyf import f as pxyf
from hak.block.is_a import f as is_block

# hstack
def f(blocks):
  if not blocks: return []
  return (_f_blocks if is_block(blocks[0]) else _f_lists_strings)(blocks)

def _f_lists_strings(blocks):
  if not blocks: return []
  blocks = normalise_heights(blocks)
  return [
    '|'.join([b[i_line] for b in blocks])
    for i_line in range(len(blocks[0]))
  ]

def _f_blocks(blocks: List[Block]) -> Block:
  if not blocks: return Block([])
  blocks = normalise_heights(blocks)
  return Block([
    '|'.join([b.get_line(i_line) for b in blocks])
    for i_line in range(blocks[0].h)
  ])

def t_lists_strings_a():
  x = []
  y = []
  return pxyf(x, y, f, new_line=1)

def t_lists_strings_b():
  u = [
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ]
  x = [u]
  y = [
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ]
  return pxyf(x, y, f, new_line=1)

def t_lists_strings_c():
  u = [
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ]
  v = [
    "---------------",
    "          Info ",
    "-----|---------",
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ]
  x = [u, v]
  y = [
    "---------|---------------",
    "    Name |          Info ",
    "---------|-----|---------",
    "         | Age | Country ",
    "---------|-----|---------",
    "   Alice |  28 |     USA ",
    "     Bob |  35 |  Canada ",
    " Charlie |  22 |      UK ",
    "---------|-----|---------",
  ]
  return pxyf(x, y, f, new_line=1)

def t_lists_strings_mismatched_heights():
  x = [['       John ', '------------', ' Rei | Zenn '], [' James ']]
  y = [
    "       John | James ",
    "------------|       ",
    " Rei | Zenn |       ",
  ]
  return pxyf(x, y, f, new_line=1)

def t_blocks_a():
  x = [Block([])]
  y = Block([])
  return pxyf(x, y, f, new_line=1)

def t_blocks_b():
  x = [Block([
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ])]
  y = Block([
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ])
  return pxyf(x, y, f, new_line=1)

def t_blocks_c():
  u = Block([
    "---------",
    "    Name ",
    "---------",
    "         ",
    "---------",
    "   Alice ",
    "     Bob ",
    " Charlie ",
    "---------",
  ])
  v = Block([
    "---------------",
    "          Info ",
    "-----|---------",
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ])
  x = [u, v]
  y = Block([
    "---------|---------------",
    "    Name |          Info ",
    "---------|-----|---------",
    "         | Age | Country ",
    "---------|-----|---------",
    "   Alice |  28 |     USA ",
    "     Bob |  35 |  Canada ",
    " Charlie |  22 |      UK ",
    "---------|-----|---------",
  ])
  return pxyf(x, y, f, new_line=1)

def t_blocks_mismatched_heights():
  x = [
    Block(['       John ', '------------', ' Rei | Zenn ']),
    Block([' James '])
  ]
  y = Block([
    "       John | James ",
    "------------|       ",
    " Rei | Zenn |       ",
  ])
  return pxyf(x, y, f, new_line=1)

def t():
  if not t_lists_strings_a(): return pf('!t_lists_strings_a')
  if not t_lists_strings_b(): return pf('!t_lists_strings_b')
  if not t_lists_strings_c(): return pf('!t_lists_strings_c')
  if not t_lists_strings_mismatched_heights():
    return pf('!t_lists_strings_mismatched_heights')
  
  if not t_blocks_a(): return pf('!t_blocks_a')
  if not t_blocks_b(): return pf('!t_blocks_b')
  if not t_blocks_c(): return pf('!t_blocks_c')
  if not t_blocks_mismatched_heights():
    return pf('!t_mismatched_heightblocks_s')

  return 1
