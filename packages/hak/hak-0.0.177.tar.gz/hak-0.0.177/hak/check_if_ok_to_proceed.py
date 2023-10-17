from queue import Queue as Q

from hak.pf import f as pf

def t_proceed():
  try: f(FakeInput(['y'])); return 1
  except RuntimeError: return pf('!t_proceed')

def t_do_not_proceed():
  try: f(FakeInput(['n'])); return pf('!t_do_not_proceed')
  except RuntimeError: return 1

t_silent = lambda: f(silent=True) == 'silent'

t = lambda: all([t_proceed(), t_do_not_proceed(), t_silent()])

class FakeInput:
  def __init__(self, input_queue):
    self.q = Q()
    for item in input_queue: self.q.put(item)
  __call__ = lambda self, prompt_text: self.q.get()

def f(x=input, silent=False):
  if silent: return 'silent'
  if x("Safe to proceed? Enter 'n' to abort:") == 'n':
    raise RuntimeError('Something is wrong')
