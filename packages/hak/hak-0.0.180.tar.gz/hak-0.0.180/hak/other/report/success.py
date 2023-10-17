from hak.string.colour.bright.green import f as success
from hak.duration import f as duration
from time import time

f = lambda name, time_started, max_filename_length: (
  True, '|'.join([
    "\r",
    f"{success('  PASS  ')}",
    f" {name:{max_filename_length}} ",
    f" {duration(time_started, name)} ",
    "",
  ])
)

def t():
  y_result = True
  y_message_l = '|'.join([
    '\r|\x1b[1;32m  PASS  \x1b[0;0m',
    ' fake_name ',
    ' \x1b[1;32m                           '
  ])
  y_message_r = '\x1b[0;0m |'
  z_result, z_message = f('fake_name', time(), 9)
  return all([
    y_result == z_result,
    y_message_l == z_message[0:len(y_message_l)],
    y_message_r == z_message[len(z_message) - len(y_message_r):]
  ])
