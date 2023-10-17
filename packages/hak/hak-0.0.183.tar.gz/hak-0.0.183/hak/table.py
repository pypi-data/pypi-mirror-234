from hak.cell import Cell
from hak.column import Column
from hak.dict.record_and_keypath.get import f as kp_to_val
from hak.dict.record.get_leaf_keypaths import f as get_leaf_keypaths
from hak.dict.to_node_tree import f as dict_to_node_tree
from hak.pf import f as pf
from hak.rate import Rate
from hak.strings.block.add_pipes_to_subseq_lines import f as add_pipes
from hak.strings.block.hstack import f as hstack
from hak.strings.block.to_str import f as block_to_str

class Table:
  def __init__(s):
    s.cells = {}
    s.row_count = 0
    s.column_keypaths = set()
    s.last_record = None

  def add_record(s, record):
    record = {'α': record}
    s.column_keypaths |= get_leaf_keypaths(record, [], set())
    s.row_count += 1
    for kp in s.column_keypaths:
      v = kp_to_val({'record': record, 'keypath': kp})
      reference = (kp, s.row_count-1)
      s.cells[reference] = Cell(v)
    s.last_record = record
    return s
    
  def add_records(s, records):
    for r in records:
      s.add_record(r)
    return s

  get_column = lambda s, column_keypath: Column(s, column_keypath)

  cols = property(lambda s: s.columns)
  columns = property(lambda s: [s.get_column(kp) for kp in s.column_keypaths])
  sorted_columns = property(lambda s: sorted(s.cols, key=lambda x: x._keypath))

  block = property(lambda s: hstack([c.block for c in s.sorted_columns]))

  def __str__(s):
    root = list(s.last_record.keys())[0]
    nodes = dict_to_node_tree(s.last_record, root=None, nodes={}, table=s)
    header_block = add_pipes(nodes[root].block[1:])
    header_str = block_to_str(header_block)
    table_str = block_to_str(s.block)
    return '\n'.join([header_str, table_str])

f = lambda: Table()

def t_table__init__():
  _t = Table()
  return all([_t.cells == {}, _t.row_count == 0, _t.column_keypaths == set()])

def t_table_add_record():
  table = Table()
  record = {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1})}}
  table.add_record(record)

  if table.column_keypaths != {('α', 'a', 'b')}:
    return pf("table.column_keypaths != {('α', 'a', 'b')}")

  if table.row_count != 1: return pf("table.row_count != 1")
  
  cell = table.cells[(('α', 'a', 'b'), 0)]
  
  if cell.value.numerator != 1:
    print(f'cell.value.numerator: {cell.value.numerator}')
    return pf('cell.value.numerator != 1')
  
  if cell.value.denominator != 3: return pf("cell.value.denominator != 3")
  
  if cell.value.unit != {'$': 1, 'm': -1}:
    return pf("cell.value.unit != {'$': 1, 'm': -1}")
  
  if table.last_record != {'α': record}:
    return pf("table.last_record != {'α': record}")

  return 1

def t_table_add_records():
  table = Table()
  records = [
    {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1}), 'c': 'abc'}},
    {'a': {'b': Rate(2, 3, {'$': 1, 'm': -1}), 'c': 'ghi'}}
  ]
  table.add_records(records)
  return len(table.cells) == 4

def t_table___str__():
  table = Table()
  records = [
    {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1}), 'c': 'abc'}},
    {'a': {'b': Rate(2, 3, {'$': 1, 'm': -1}), 'c': 'ghi'}}
  ]
  table.add_records(records)
  y = '\n'.join([
    '-----------',
    '     a     ',
    '-----------',
    '  b  |  c  ',
    '-----|-----',
    ' $/m |     ',
    '-----|-----',
    ' 1/3 | abc ',
    ' 2/3 | ghi ',
    '-----|-----'
  ])
  z = str(table)
  return y == z

def t_table_get_column():
  table = Table()
  records = [
    {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1}), 'c': 'abc'}},
    {'a': {'b': Rate(2, 3, {'$': 1, 'm': -1}), 'c': 'ghi'}}
  ]
  table.add_records(records)
  column = table.get_column(('α', 'a', 'b'))
  return column.block == ['-----', ' $/m ', '-----', ' 1/3 ', ' 2/3 ', '-----']

def t_table_columns():
  table = Table()
  records = [
    {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1}), 'c': 'abc'}},
    {'a': {'b': Rate(2, 3, {'$': 1, 'm': -1}), 'c': 'ghi'}}
  ]
  table.add_records(records)
  y_table_column_blocks = [
    ['-----', '     ', '-----', ' abc ', ' ghi ', '-----'],
    ['-----', ' $/m ', '-----', ' 1/3 ', ' 2/3 ', '-----'],
  ]
  
  z_table_column_blocks = set([str(c.block) for c in table.columns])

  return all([
    str(y_table_column_block) in z_table_column_blocks
    for y_table_column_block
    in y_table_column_blocks
  ])

def t_table_block():
  table = Table()
  records = [
    {'a': {'b': Rate(1, 3, {'$': 1, 'm': -1}), 'c': 'abc'}},
    {'a': {'b': Rate(2, 3, {'$': 1, 'm': -1}), 'c': 'ghi'}}
  ]
  table.add_records(records)
  y_blocks = [
    ['-----', '     ', '-----', ' abc ', ' ghi ', '-----'],
    ['-----', ' $/m ', '-----', ' 1/3 ', ' 2/3 ', '-----'],
    ['-----', '     ', '-----', ' abc ', ' ghi ', '-----'],
    ['-----', ' $/m ', '-----', ' 1/3 ', ' 2/3 ', '-----']
  ]
  c_blocks = [c.block for c in table.columns]
  for i in range(len(table.columns)):
    c = table.columns[i]
    if y_blocks[i] not in c_blocks:
      return pf(f'y_blocks[i] != c.block; {y_blocks[i]} != {c.block}')
  return 1

def t():
  if not t_table__init__(): return pf('!t_table__init__')
  if not t_table_add_record(): return pf('!t_table_add_record')
  if not t_table_add_records(): return pf('!t_table_add_records')
  if not t_table___str__(): return pf('!t_table___str__')
  if not t_table_get_column(): return pf('t_table_get_column')
  if not t_table_columns(): return pf('t_table_columns')
  if not t_table_block(): return pf('t_table_block')
  return 1
