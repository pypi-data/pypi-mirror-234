from hak.string.colour.bright.magenta import f as magenta
from hak.string.colour.bright.blue import f as blue
from hak.string.colour.bright.red import f as red
from hak.string.colour.bright.cyan import f as cy
from hak.string.colour.bright.green import f as green

f = lambda w: {0: green, 1: cy, 2: blue, 3: magenta, 4: red}[w//5]

t = lambda: all([
  *[green == f(_) for _ in range(5)],
  *[cy == f(_) for _ in range(5, 10)],
  *[blue == f(_) for _ in range(10, 15)],
  *[magenta == f(_) for _ in range(15, 20)],
  *[red == f(_) for _ in range(20, 24)],
])
