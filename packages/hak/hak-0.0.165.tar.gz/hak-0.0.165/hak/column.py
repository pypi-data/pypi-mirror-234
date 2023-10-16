from hak.dict.char_and_width.to_str import f as make_homogenous_line
from hak.dict.value_and_width.to_str import f as fvw
from hak.pf import f as pf
from hak.rate import Rate
from hak.string.colour.bright.green import f as green
from hak.string.colour.decolour import f as decol

class Column:
  def __init__(self, table, keypath):
    self._keypath = keypath
    self._name = self._keypath[-1]
    self._table = table
    self._type = None
    self._unit = None
    self._include_heading = False

  w = property(
    lambda s: max([
      len(s._name),
      *[len(decol(str(c))) for c in s.cells],
      *[len(c.get_unit_str()) for c in s.cells]
    ])
  )
  width = property(lambda s: s.w)

  def _get_cells(self):
    result = []
    for r in range(self._table.row_count):
      d = self._table.cells
      kp = (self._keypath, r)
      if kp in d:
        cell = d[kp]
        result.append(cell)
    return result

  cells = property(_get_cells)

  def _to_block(self):
    w = self.width
    cell_strings = [fvw({'value': c, 'width': w}) for c in self.cells]
    bar = make_homogenous_line({'char': '-', 'width': w})
    heading = [bar, fvw({'value': self._name, 'width': w})]

    result_excl_heading = [
      bar,
      fvw({'value': self.cells[0].get_unit_str(), 'width': w}),
      bar,
      *cell_strings,
      bar,
    ]

    result_incl_heading = heading + result_excl_heading

    return result_incl_heading if self._include_heading else result_excl_heading

  block = property(_to_block)

  __str__ = lambda self: '\n'.join(self.block)

def f(table, keypath): Column(table, keypath)

def t_column_a(T):
  _table = T()
  x = {'table': _table, 'keypath': ('α', 'abc', 'def', 'ghi')}
  z = Column(**x)
  if not z._keypath == x['keypath']: return pf("!: z._keypath == x['keypath']")
  if not z._name == 'ghi': return pf("!: z._name == 'ghi'")
  if not z._table == _table: return pf("!: z._table == _table")
  if not z._type == None: return pf("!: z._type == None")
  if not z._unit == None: return pf("!: z._unit == None")
  if not z._include_heading == 0: return pf("!: z._include_heading == False")
  return 1

def t_column_b_column_name(T):
  x = {'table': T(), 'keypath': ('α', 'abc', 'def', 'ghi')}
  z = Column(**x)
  result = all([z.w == len(x['keypath'][-1]), z.width == len(x['keypath'][-1])])
  return result

def t_column_b_decol_cell_strs(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': green('YY')}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  result = column.w == 2
  return result

def t_column_b_unit_str_len(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  result = column.w == len('$/m')
  return result

def t_column_b(T):
  if not t_column_b_column_name(T): return pf('!t_b_column_name')
  if not t_column_b_decol_cell_strs(T): return pf('!t_b_decol_cell_strs')
  if not t_column_b_unit_str_len(T): return pf('!t_b_unit_str_len')
  return 1

def t_column_c(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(121, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(122, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  cells = column._get_cells()
  return [str(c) for c in cells] == ['1/2', '121/240', '61/120']

def t_column_d(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  return column.cells == column._get_cells()

def t_column_e_exclude_heading(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(121, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(122, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  return column._to_block() == [
    '---------',
    '     $/m ',
    '---------',
    '     1/2 ',
    ' 121/240 ',
    '  61/120 ',
    '---------'
  ]

def t_column_e_include_heading(T):
  _table = T()
  _rate = Rate(120, 240, {'$': 1, 'm': -1})
  record = {'a': {'d': {'g': _rate}}}
  _table.add_record(record)
  column = _table.get_column(('α', 'a', 'd', 'g'))
  column._include_heading = True
  y = [
    '-----',
    '   g ',
    '-----',
    ' $/m ',
    '-----',
    ' 1/2 ',
    '-----'
  ]
  z = column._to_block()
  return y == z or pf([f'y: {y}', f'z: {z}'])

def t_column_e(T):
  if not t_column_e_exclude_heading(T): return pf('!t_column_e_exclude_heading')
  if not t_column_e_include_heading(T): return pf('!t_column_e_include_heading')
  return 1

def t_column_f(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  return column.block == column._to_block()

def t_column_g(T):
  _table = T()
  _table.add_record({'a': {'d': {'g': Rate(120, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(121, 240, {'$': 1, 'm': -1})}}})
  _table.add_record({'a': {'d': {'g': Rate(122, 240, {'$': 1, 'm': -1})}}})
  column = _table.get_column(('α', 'a', 'd', 'g'))
  y = '\n'.join([
    '---------',
    '     $/m ',
    '---------',
    '     1/2 ',
    ' 121/240 ',
    '  61/120 ',
    '---------'
  ])
  z = str(column)
  return y == z

def t():
  from importlib import import_module
  T = import_module('hak.table').Table
  if not t_column_a(T): return pf('!t_a')
  if not t_column_b(T): return pf('!t_b')
  if not t_column_c(T): return pf('!t_c')
  if not t_column_d(T): return pf('!t_d')
  if not t_column_e(T): return pf('!t_e')
  if not t_column_f(T): return pf('!t_f')
  if not t_column_g(T): return pf('!t_g')
  return 1
