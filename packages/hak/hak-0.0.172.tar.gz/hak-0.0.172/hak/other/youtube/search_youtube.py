#coding=utf-8
import webbrowser
from hak.other.youtube.identifier.japanese.make import f as gen_jid

def f():
  for _ in range(10):
    webbrowser.open_new_tab(
      f'https://www.youtube.com/results?search_query={gen_jid()}'
    )

t = lambda: 1
