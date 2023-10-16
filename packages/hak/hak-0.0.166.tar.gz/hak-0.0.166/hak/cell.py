from hak.bool.is_a import f as is_bool
from hak.dict.rate.is_a import f as is_rate # TODO: Delete?
from hak.dict.rate.to_str_frac import f as rate_to_str # TODO: Delete?
from hak.dict.unit.to_str import f as unit_to_str
from hak.get_datatype import f as detect_type
from hak.is_0 import f as is_0
from hak.is_none import f as is_none
from hak.number.float.is_a import f as is_float
from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.rate import Rate
from hak.string.colour.bright.green import f as green
from hak.string.colour.bright.red import f as red
from hak.string.colour.decolour import f as decol

class Cell:
  def __init__(self, value):
    self.value = value
    self.type = 'Rate' if isinstance(value, Rate) else detect_type(value)

  def __str__(self):
    v = self.value
    if  is_none(v): return ''
    if  is_rate(v): return rate_to_str(v)
    if  is_bool(v): return green('Y') if v else red('N')
    if     is_0(v): return ''
    if is_float(v): return f"{v:.2f}"
    return str(v)

  get_unit_str = lambda self: (
    unit_to_str(self.value.unit)
    if self.type == 'Rate' else
    ''
  )
  
  width = property(lambda self: max([
    len(decol(str(self))),
    len(decol(self.get_unit_str())),
  ]))

f = lambda x: Cell(x)

def t_cell_a():
  x = Cell(0)
  y = ''
  z = str(x)
  return pxyz(x, y, z)

def t_cell_b():
  x = Cell('abc')
  y = 'abc'
  z = str(x)
  return pxyz(x, y, z)

def t_cell_c():
  x = Cell(123)
  y = '123'
  z = str(x)
  return pxyz(x, y, z)

def t_cell_d():
  x = Cell(1.3)
  y = '1.30'
  z = str(x)
  return pxyz(x, y, z)

def t_cell_e():
  x = Cell(True)
  y = green('Y')
  z = str(x)
  return pxyz(x, y, z)

def t_cell_f():
  x = Cell(False)
  y = red('N')
  z = str(x)
  return pxyz(x, y, z)

def t_cell_g():
  value = Rate(numerator=120, denominator=240, unit={'$': 1, 'm': -1})
  x = Cell(value)
  y = '1/2'
  z = str(x)
  return pxyz(x, y, z)

def t():
  if not t_cell_a(): return pf('!t_cell_a')
  if not t_cell_b(): return pf('!t_cell_b')
  if not t_cell_c(): return pf('!t_cell_c')
  if not t_cell_d(): return pf('!t_cell_d')
  if not t_cell_e(): return pf('!t_cell_e')
  if not t_cell_f(): return pf('!t_cell_f')
  if not t_cell_g(): return pf('!t_cell_g')
  return 1
