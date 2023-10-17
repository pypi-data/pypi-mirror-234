from hak.classes.block import Block

# is_block
f = lambda b: isinstance(b, Block)
t = lambda: all([f(Block(['---', '   ', '---'])), not f(['---', '   ', '---'])])
