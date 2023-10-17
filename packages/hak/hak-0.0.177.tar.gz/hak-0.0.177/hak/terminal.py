from hak.system.screen.clear import f as clear_screen
from hak.pf import f as pf

class Terminal:
  __init__ = lambda self, mode='run': self.reset(mode)

  def print(self, string:str='', end='\n'):
    if self.mode == 'test':
      self.output_stream_as_list.append(string+end)
    else:
      print(string, end=end)
    return string

  input = lambda self, string='': (
    self.input_stream_as_list.pop() if self.mode == 'test' else input(string)
  )

  def reset(self, mode='run'):
    self.reset_stream_lists()
    self.mode = mode

  def reset_stdo(self): self.output_stream_as_list = []
  def reset_stdi(self): self.input_stream_as_list = []

  def reset_stream_lists(self):
    self.reset_stdi()
    self.reset_stdo()
  
  def clear(self, cls=None):
    self.reset_stdo()
    return (clear_screen if self.mode == 'run' else lambda: True)()

f = lambda mode='run': Terminal(mode)

def t_clear():
  terminal = f('test')
  terminal.print('abc')
  result = terminal.clear()
  return all([terminal.output_stream_as_list == [], result])

def t_term_print():
  terminal = f('test')
  data = 'abc'
  result = terminal.print(data)

  if terminal.output_stream_as_list != [data+'\n']: return pf([
    'terminal.output_stream_as_list != [data+"\n"]',
    f'terminal.output_stream_as_list: {terminal.output_stream_as_list}',
    f'[data]:                         {[data]}'
  ])

  if result != data: return pf([
    'result != data',
    f'[result]: {[result]}',
    f'[data]:   {[data]}'
  ])
  
  return 1

def t_term_input():
  terminal = f('test')
  terminal.input_stream_as_list.append('response text')
  return terminal.input('prompt text') == 'response text'

def t_term_reset():
  terminal = f('test')

  terminal.mode = 'xyz'
  terminal.input_stream_as_list.append('abc')
  terminal.output_stream_as_list.append('ghi')
  terminal.reset()
      
  return all([
    terminal.mode == 'run',
    terminal.input_stream_as_list == [],
    terminal.output_stream_as_list == []
  ])

def t_term_reset_stdo():
  terminal = f('test')
  terminal.output_stream_as_list.append('ghi')
  terminal.reset_stdo()
  return terminal.output_stream_as_list == []

def t_term_reset_stdi():
  terminal = f('test')
  terminal.input_stream_as_list.append('ghi')
  terminal.reset_stdi()
  return terminal.input_stream_as_list == []

def t_term_reset_strm_lists():
  terminal = f('test')
  terminal.output_stream_as_list.append('abc')
  terminal.input_stream_as_list.append('ghi')
  terminal.reset_stream_lists()
  return all([
    terminal.output_stream_as_list == [],
    terminal.input_stream_as_list == []
  ])

def t():
  if not t_term_print(): return pf(['not t_term_print()'])
  if not t_term_input(): return pf(['not t_term_input()'])
  if not t_term_reset(): return pf(['not t_term_reset()'])
  if not t_term_reset_stdo(): return pf(['!t_term_reset_stdo()'])
  if not t_term_reset_stdi(): return pf(['!t_term_reset_stdi()'])
  if not t_term_reset_strm_lists(): return pf(['not t_term_reset_strm_lists()'])
  if not t_clear(): return pf(['not t_clear()'])
  return 1
