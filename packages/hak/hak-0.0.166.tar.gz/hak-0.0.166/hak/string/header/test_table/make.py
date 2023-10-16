w_max = 23

def f(max_filename_length):
  hak_name = "Name"
  duration_ms = "Duration [ms]"
  w = w_max + 10
  return '\n'.join([
    f"| Result | {hak_name:{max_filename_length}} | {duration_ms:^{w}}| ",
    f"|--------|-" + "-"*max_filename_length +"-|-" + "-"*w+"|"  
  ])

t = lambda: '\n'.join([
  '| Result | Name                 |           Duration [ms]          | ',
  '|--------|----------------------|----------------------------------|'
]) == f(20)
