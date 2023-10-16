from hak.dict.rate.make import f as mk_rate
from hak.dicts.get_all_keys import f as get_field_names
from hak.pxyf import f as pxyf
from hak.values.get_datatype import f as detect_datatype_from_values

# src.table.fields.datatypes.get
f = lambda x: {
  k: detect_datatype_from_values([d[k] if k in d else None for d in x])
  for k in get_field_names(x)
}

t = lambda: pxyf(
  [
    {'a': True,  'b': 'abc', 'c': mk_rate(1.23, 1, {'m': 1})},
    {'a': True,  'b': 'def', 'c': mk_rate(1.23, 1, {'m': 1})},
    {'a': False, 'b': 'ghi', 'c': mk_rate(1.23, 1, {'m': 1})},
  ],
  {'a': 'bool', 'b': 'str', 'c': 'rate'},
  f
)
