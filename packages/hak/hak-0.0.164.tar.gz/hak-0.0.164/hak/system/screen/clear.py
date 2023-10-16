from os import system
from os import name

from hak.fake.os.system import f as fake_system
from hak.fake.printer import f as fake_printer

def f(sys=system, os_name=name, prnt=print):
  try: sys({'nt': 'cls', 'posix': 'clear',}[os_name])
  except KeyError as ke: prnt(f'Only implemented for nt or posix systems. {ke}')

def t_nt():
  fake_sys = fake_system()
  f(sys=fake_sys, os_name='nt')
  return fake_sys.history[-1] == 'cls'

def t_posix():
  fake_sys = fake_system()
  f(sys=fake_sys, os_name='posix')
  return fake_sys.history[-1] == 'clear'

def t_key_error():
  fp = fake_printer()
  fake_sys = fake_system()
  f(sys=fake_sys, os_name='ke', prnt=fp)
  return fp.history == ["Only implemented for nt or posix systems. 'ke'"]

t = lambda: all([t_nt(), t_posix(), t_key_error()])
