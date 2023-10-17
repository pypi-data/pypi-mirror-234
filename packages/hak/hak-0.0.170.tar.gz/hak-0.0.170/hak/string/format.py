# ignore_overlength_linesontain version
from .append.new_line import f as append_new_line
from .colour.bright.cyan import f as cy
from .colour.bright.magenta import f as magenta
from .colour.bright.yellow import f as yellow
from .indent.run_if_class_method import f as indent_if_is_run_method
from .insert.new_line_after_last_import_line import f as place_blank_line_after_last_import_line
from .insert.new_line_before_comment import f as insert_nl_before_comment
from .insert.new_line_before_def import f as insert_nl_before_def
from .insert.new_line_before_if_main import f as insert_nl_before_if_main
from .insert.new_line_before_lambda import f as add_nl_before_lambda_methods
from .insert.new_line_before_lambda import f as insert_nl_before_lambda
from .insert.new_line_before_new_line_and_cea_ import f as insert_nl_before_nl_and_cea_
from .remove.empty_line_spaces import f as remove_empty_line_spaces
from .remove.extra_new_line_following_class_definition import f as remove_gap_following_class_definition
from .remove.first_new_line_if_starts_with_new_line import f as remove_first_nl_if_file_starts_with_newline
from .remove.whitespace_between_newlines import f as remove_whitespace_between_newlines
from .replace.double_new_line_with_single_new_line import f as replace_double_nl_with_single_new_line
from .replace.single_new_line_with_empty_string import f as replace_single_nl_content_with_empty_string
from .replace.triple_new_line_with_double_new_line import f as replace_triple_newlines_with_double_newlines
from hak.strings.compare import f as compare_strings

def f(x: str):
  for fn in [
    append_new_line,
    replace_double_nl_with_single_new_line,
    remove_empty_line_spaces,
    insert_nl_before_def,
    insert_nl_before_lambda,
    insert_nl_before_if_main,
    insert_nl_before_comment,
    insert_nl_before_nl_and_cea_,
    add_nl_before_lambda_methods,
    place_blank_line_after_last_import_line,
    replace_triple_newlines_with_double_newlines,
    replace_single_nl_content_with_empty_string,
    remove_gap_following_class_definition,
    remove_first_nl_if_file_starts_with_newline,
    remove_first_nl_if_file_starts_with_newline,
    indent_if_is_run_method,
    remove_whitespace_between_newlines
  ]:
    x = fn(x)
  return x

def t():
  x = '\n'.join([
    '',
    '# abc',
    '# ghi',
    'from goo import goo',
    'from boo import boo',
    'run = lambda x: x*x',
    'def main():',
    '  print("main")',
    '',
    '',
    "if __name__ == '__main__':",
    '  main()',
    '\n  \n',
    'class FakeInput:',
    '  def __init__(self, input_queue):',
    '    self.q = Q()',
    '    for item in input_queue:',
    '      self.q.put(item)',
    '  ',
    '  def __call__(self, prompt_text):',
    '    return self.q.get()',
    'run = lambda self: None',
    '',
    'def run(inp=input):',
    '  if inp("Safe to proceed? Enter n to abort:") == "n":',
    '    raise RuntimeError("Something is wrong")',
    '',
    'def t_proceed_path():',
    '  fi = FakeInput(["y"])',
    '  try:',
    '    run(fi)',
    '    return 1',
    '  except RuntimeError:',
    '    return 0',
    '',
    'def t_do_not_proceed_path():',
    '  fi = FakeInput(["n"])',
    '  try:',
    '    run(fi)',
    '    return 0',
    '  except RuntimeError:',
    '    return 1',
    '',
    'test = lambda: all([',
    '  t_proceed_path(),',
    '  t_do_not_proceed_path()',
    '])',
  ])
  z = f(x)
  y = '\n'.join([
    '# abc',
    '',
    '# ghi',
    'from goo import goo',
    'from boo import boo',
    '',
    'run = lambda x: x*x',
    '',
    'def main():',
    '  print("main")',
    '',
    "if __name__ == '__main__':",
    '  main()',
    '',
    'class FakeInput:',
    '  def __init__(self, input_queue):',
    '    self.q = Q()',
    '    for item in input_queue:',
    '      self.q.put(item)',
    '',
    '  def __call__(self, prompt_text):',
    '    return self.q.get()',
    '',
    '  run = lambda self: None',
    '',
    'def run(inp=input):',
    '  if inp("Safe to proceed? Enter n to abort:") == "n":',
    '    raise RuntimeError("Something is wrong")',
    '',
    'def t_proceed_path():',
    '  fi = FakeInput(["y"])',
    '  try:',
    '    run(fi)',
    '    return 1',
    '  except RuntimeError:',
    '    return 0',
    '',
    'def t_do_not_proceed_path():',
    '  fi = FakeInput(["n"])',
    '  try:',
    '    run(fi)',
    '    return 0',
    '  except RuntimeError:',
    '    return 1',
    '',
    'test = lambda: all([',
    '  t_proceed_path(),',
    '  t_do_not_proceed_path()',
    '])',
    ''
  ])
  test_result = y == z
  if not test_result:
    for _ in [
      'x:', '-'*80, yellow(x), '-'*80, '',
      'y:', '-'*80, magenta(y), '-'*80, '',
      'z:', '-'*80, cy(z), '-'*80, '',
    ]:
      print(_)
    
    result = compare_strings(y, z)
    if len(result) == 3:
      x, y, i = result
      w = 20
      print(z[i-w:i-1]+cy(z[i])+z[i+1:i+w])
      print(y[i-w:i+w])
    else:
      print(result)
  return test_result
