# m_name_to_m_index
def f(x):
  _x = x.title()[:3]
  return {
    'Jan': 0,
    'Feb': 1,
    'Mar': 2,
    'Apr': 3,
    'May': 4,
    'Jun': 5,
    'Jul': 6,
    'Aug': 7,
    'Sep': 8,
    'Oct': 9,
    'Nov': 10,
    'Dec': 11
  }[_x]

t = lambda: all([f('January') == 0, f('July') == 6])
