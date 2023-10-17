from hak.classes.block import Block
from hak.pxyf import f as pxyf

f = lambda x: Block(
  [x.lines[0]]+
  [
    x.lines[i]
    for i
    in range(1, x.h)
    if not all([x.lines[i-1] == ' '*80, x.lines[i] == ' '*80])
  ]
)

_hbar = '-'*80
_sp20 = ' '*20

def t():
  x = Block([
    _hbar,
    "                                 Lawn Services",
    '                              Comprehensive Income',
    "                        for the month ending 2021-05-31",
    _hbar,
    "Expenses                           "+_sp20+"                   155.00",
    "  Depreciation                     "+_sp20+"          70.00",
    "  Fuel                             "+_sp20+"          80.00",
    "  Interest                         "+_sp20+"           5.00",
    "",
    "Revenues                           "+_sp20+"                  1120.00",
    "  Sales                            "+_sp20+"        1120.00",
    "",
    "",
    "Net Profit                         "+_sp20+"                   965.00",
    _hbar,
  ])
  y = Block([
    _hbar,
    "                                 Lawn Services",
    '                              Comprehensive Income',
    "                        for the month ending 2021-05-31",
    _hbar,
    "Expenses                           "+_sp20+"                   155.00",
    "  Depreciation                     "+_sp20+"          70.00",
    "  Fuel                             "+_sp20+"          80.00",
    "  Interest                         "+_sp20+"           5.00",
    "",
    "Revenues                           "+_sp20+"                  1120.00",
    "  Sales                            "+_sp20+"        1120.00",
    "",
    "Net Profit                         "+_sp20+"                   965.00",
    _hbar,
  ])
  return pxyf(x, y, f, new_line=1)
