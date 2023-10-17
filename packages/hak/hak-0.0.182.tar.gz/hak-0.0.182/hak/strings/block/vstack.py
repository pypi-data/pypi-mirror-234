from hak.block.is_a import f as is_block
from hak.classes.block import Block
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# vstack
f = lambda blocks: (
  (_f_blocks if is_block(blocks[0]) else _f_lists_strings)(blocks)
  if blocks
  else []
)
  
def _f_lists_strings(blocks):
  lines = []
  w = len(blocks[0][0])
  for b in blocks[:-1]:
    lines += b + ['-'*w]
  lines += blocks[-1]
  return lines

def _f_blocks(blocks):
  lines = []
  w = blocks[0].w
  for b in blocks[:-1]:
    lines += b.lines + ['-'*w]
  lines += blocks[-1].lines
  return Block(lines)

def t_lists_strings():
  u = [
    "---------------",
    "          Info ",
  ]
  v = [
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ]
  x = [u, v]
  y = [
    "---------------",
    "          Info ",
    "---------------",
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ]
  return pxyf(x, y, f, new_line=1)

def t_blocks():
  u = Block([
    "---------------",
    "          Info ",
  ])
  v = Block([
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ])
  x = [u, v]
  y = Block([
    "---------------",
    "          Info ",
    "---------------",
    " Age | Country ",
    "-----|---------",
    "  28 |     USA ",
    "  35 |  Canada ",
    "  22 |      UK ",
    "-----|---------",
  ])
  return pxyf(x, y, f, new_line=1)

def t():
  if not t_lists_strings(): return pf('!t_lists_strings')
  if not t_blocks(): return pf('!t_blocks')
  return 1
