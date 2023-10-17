from hak.pxyf import f as pxyf

# _get_max_block_height
f = lambda blocks: max([len(block) for block in blocks])

def t():
  x = [[' james '], ['    john    ', '------------', ' rei | zenn ']]
  y = 3
  return pxyf(x, y, f)
