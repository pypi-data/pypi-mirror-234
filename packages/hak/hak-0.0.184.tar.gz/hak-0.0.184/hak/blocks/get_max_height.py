from hak.block.is_a import f as is_block
from hak.classes.block import Block
from hak.pf import f as pf
from hak.pxyf import f as pxyf

# _get_max_block_height
f = lambda blocks: max([b.h if is_block(b) else len(b) for b in blocks])

t_blocks = lambda: pxyf(
  [
    Block([' james ']),
    Block([
      '    john    ',
      '------------',
      ' rei | zenn '
    ])
  ],
  3,
  f
)

t_strings = lambda: pxyf(
  [
    [' james '],
    [
      '    john    ',
      '------------',
      ' rei | zenn '
    ]
  ],
  3,
  f
)

def t():
  if not t_blocks(): return pf('!t_blocks')
  if not t_strings(): return pf('!t_strings')
  return 1
