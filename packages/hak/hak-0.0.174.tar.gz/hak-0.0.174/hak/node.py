from hak.numbers.ints.cell_value_widths.to_aggregate_width import f as aw
from hak.strings.block.hstack import f as hstack
from hak.strings.block.vstack import f as vstack
from hak.pf import f as pf

class Node:
  def __init__(s, name, table):
    s.name = name
    s.children = set()
    s.nodepath = tuple([name])
    s.table = table

  def add_child(s, child):
    s.children.add(child)
    child.nodepath = tuple(list(s.nodepath)+ list(child.nodepath))

  def add_children(s, children):
    for c in children:
      s.add_child(c)

  def _make_block(x):
    top_block = [f' {x.name:^{x.width}} ']
    return (
      vstack([
        top_block,
        hstack([c.block for c in x.sort_children_by_nodepath()])
      ])
      if x.children else
      top_block
    )

  block = property(_make_block)

  _get_width = lambda node: max(
    len(node.name),
    aw([c.width for c in node.children]),
    (
      node.table.get_column(node.nodepath).width
      if (node.nodepath, 0) in node.table.cells else
      0
    )
  )

  width = property(_get_width)

  sort_children_by_nodepath = lambda s: sorted(
    s.children,
    key=lambda x: x.nodepath
  )

f = lambda name, table: Node(name, table)

def t_node__init(T):
  _table = T()
  node = Node('node_name', _table)
  if node.name != 'node_name': return pf("node.name != 'node_name'")
  if node.children != set(): return pf("node.children != set()")
  if node.nodepath != tuple(['node_name']):
    return pf("node.nodepath != tuple(['node_name'])")
  if node.table != _table: return pf("node.table != _table")
  return 1

def t_node__str(T): return 0 # TODO
def t_node_add_child(T): return 0 # TODO
def t_node_add_children(T): return 0 # TODO
def t_node_block(T): return 0 # TODO
def t_node_level(T): return 0 # TODO
def t_node_width(T): return 0 # TODO

def t_sort_children_by_nodepath(T):
  _t = T()
  _n = Node('root', _t)
  children_names = ['xyz', 'uvw', 'mno', 'abc']
  children = [Node(child_name, _t) for child_name in children_names]
  _n.add_children(children)
  return all([c.name in children_names for c in _n.children])

def t():
  from importlib import import_module
  T = import_module('hak.table').Table
  if not t_node__init(T): return pf('!t_node__init')

  if not t_sort_children_by_nodepath(T):
    return pf('!t_sort_children_by_nodepath')

  # if not t_node__str(T): return pf('!t_node__str')
  # if not t_node_add_child(T): return pf('!t_node_add_child')
  # if not t_node_add_children(T): return pf('!t_node_add_children')
  # if not t_node_block(T): return pf('!t_node_block')
  # if not t_node_level(T): return pf('!t_node_level')
  # if not t_node_width(T): return pf('!t_node_width')
  return 1
