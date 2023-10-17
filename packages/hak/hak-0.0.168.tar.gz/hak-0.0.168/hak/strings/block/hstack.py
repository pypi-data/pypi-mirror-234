from hak.pxyf import f as pxyf
from hak.pf import f as pf
from hak.blocks.normalise_heights import f as normalise_block_heights

# hstack
def f(blocks):
  if not blocks: return []
  blocks = normalise_block_heights(blocks)
  return ['|'.join([x_i[j] for x_i in blocks]) for j in range(len(blocks[0]))]

def t_a():
  x = []
  y = []
  return pxyf(x, y, f, new_line=1)

def t_b():
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

def t_c():
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

def t_mismatched_heights():
  x = [['       John ', '------------', ' Rei | Zenn '], [' James ']]
  y = [
    "       John | James ",
    "------------|       ",
    " Rei | Zenn |       ",
  ]
  return pxyf(x, y, f, new_line=1)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_mismatched_heights(): return pf('!t_mismatched_heights')
  return 1
