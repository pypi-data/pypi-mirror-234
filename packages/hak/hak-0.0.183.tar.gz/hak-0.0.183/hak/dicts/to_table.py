# ignore_overlength_lines

from datetime import date
from hak.dicts.flat.homogenise import f as homogenise_dicts
from hak.pf import f as pf
from hak.pxyz import f as pxyz
from hak.rate import Rate
from hak.table import Table
from hak.pxyf import f as pxyf

f = lambda x: str(Table().add_records(homogenise_dicts(x)))

def t_a():
  x = [
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 0, 'rei': 1}, 'james': 'abcxyz'},
        'wendi': {'bec': {'theo': 3.14159, 'max': 3.149}},
        'liz': True,
        'donald': 6,
        'price': Rate(1, 2, {'$': 1, 'item': -1})
      }
    },
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 7, 'rei': 8}, 'james': 'defuvw'},
        'wendi': {'bec': {'theo': 10, 'max': 11}},
        'liz': True,
        'donald': None,
        'price': Rate(2, 3, {'$': 1, 'item': -1})
      }
    },
    {
      'date': date(2023, 1, 1),
      'cecil': {
        'robert': {'john': {'zenn': 14, 'rei': 15}, 'james': 'ghipqrs'},
        'wendi': {'bec': {'theo': 17, 'max': 18}},
        'liz': False,
        'donald': 20,
        'price': Rate(4, 5, {'$': 1, 'item': -1})
      }
    }
  ]
  y = '\n'.join([
    '-------------------------------------------------------------------------',
    '                           cecil                            |    date    ',
    '------------------------------------------------------------|            ',
    ' donald | liz | price  |        robert        |    wendi    |            ',
    '        |     |        |----------------------|-------------|            ',
    '        |     |        |  james  |    john    |     bec     |            ',
    '        |     |        |         |------------|-------------|            ',
    '        |     |        |         | rei | zenn | max  | theo |            ',
    '--------|-----|--------|---------|-----|------|------|------|------------',
    '        |     | $/item |         |     |      |      |      |            ',
    '--------|-----|--------|---------|-----|------|------|------|------------',
    '      6 |   \x1b[1;32mY\x1b[0;0m |    1/2 |  abcxyz |   1 |      | 3.15 | 3.14 | 2023-01-01 ',
    '        |   \x1b[1;32mY\x1b[0;0m |    2/3 |  defuvw |   8 |    7 |   11 |   10 | 2023-01-01 ',
    '     20 |   \x1b[1;31mN\x1b[0;0m |    4/5 | ghipqrs |  15 |   14 |   18 |   17 | 2023-01-01 ',
    '--------|-----|--------|---------|-----|------|------|------|------------'
  ])

  return pxyf(x, y, f)

def t_b():
  x = [
    {
      'date': date(2023, 1, 1),
      # This dict is missing the key 'notes'
    },
    {
      'date': date(2023, 1, 1),
      'notes': 'This note is longer than the heading.'
    },
    {
      'date': date(2023, 1, 1),
      'notes': ''
    }
  ]
  y = '\n'.join([
    '----------------------------------------------------',
    '    date    |                 notes                 ',
    '------------|---------------------------------------',
    '            |                                       ',
    '------------|---------------------------------------',
    ' 2023-01-01 |                                       ',
    ' 2023-01-01 | This note is longer than the heading. ',
    ' 2023-01-01 |                                       ',
    '------------|---------------------------------------'
  ])
  return pxyf(x, y, f, new_line=1)

def t_c():
  x = [
    {
      'date': date(2023, 1, 1),
      'A': {'cash': {'primary': 0, 'secondary': 1}},
      'cash_flow': {'amount': 2, 'name': 'three', 'type': 'four'}
    },
    {
      'date': date(2023, 1, 1),
      'A': {'cash': {'primary': 5, 'secondary': 6}},
      'cash_flow': {'amount': 7, 'name': 'eight', 'type': 'nine'}
    },
    {
      'date': date(2023, 1, 1),
      'A': {'cash': {'primary': 10, 'secondary': 11}},
      'cash_flow': {'amount': 12, 'name': 'thirteen', 'type': 'fourteen'}
    }
  ]
  y = '\n'.join([
    '-----------------------------------------------------------------',
    '          A          |          cash_flow           |    date    ',
    '---------------------|------------------------------|            ',
    '        cash         | amount |   name   |   type   |            ',
    '---------------------|        |          |          |            ',
    ' primary | secondary |        |          |          |            ',
    '---------|-----------|--------|----------|----------|------------',
    '         |           |        |          |          |            ',
    '---------|-----------|--------|----------|----------|------------',
    '         |         1 |      2 |    three |     four | 2023-01-01 ',
    '       5 |         6 |      7 |    eight |     nine | 2023-01-01 ',
    '      10 |        11 |     12 | thirteen | fourteen | 2023-01-01 ',
    '---------|-----------|--------|----------|----------|------------',
  ])
  return pxyf(x, y, f, new_line=1)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  return 1

if __name__ == '__main__':
  result = t()
  print(int(result), end='')
