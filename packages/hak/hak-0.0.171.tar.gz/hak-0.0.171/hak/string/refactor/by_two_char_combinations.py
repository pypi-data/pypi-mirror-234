from subprocess import run as sprun
from hak.strings.two_char_combinations import f as prepare_combinations

def f(original):
  data = original
  chars = ''.join(sorted(list(set(data))))
  _L = prepare_combinations(chars)
  for _l in _L:
    candidate_data = data.replace(_l, '')
    if len(candidate_data) < len(data):
      _raw_result = sprun(
        args=[ 'python3', '-c', candidate_data],
        capture_output=True
      )
      _decoded_stdout = _raw_result.stdout.decode()
      if len(_decoded_stdout) > 0:
        try: result = eval(_decoded_stdout)
        except SyntaxError as se: result = False
        if result: data = candidate_data
  return len(original)>len(data), data

def t():
  original_content = '\n'.join([
    "def foo(x):",
    "  return x*x",
    "",
    "def test():",
    "  y = 16",
    "  z = foo(4)",
    "  return y == z",
    "",
    "if __name__=='__main__':print(test())",
  ])
  change_made, z = f(original_content)
  return all([change_made, z=='\n'.join([
    "def o(x):",
    "  return x*x",
    "",
    "def tt():",
    "  y = 16",
    "  z = o(4)",
    "  return y == z",
    "",
    "if __name__=='__main__':print(tt())",
  ])])

if __name__=='__main__': print(t())
