def f(x):
  x = x.replace('\ndef ', '\n\ndef ')
  x = x.replace('\n  def ', '\n\n  def ')
  return x

def t():
  y_0 = '\n\ndef '
  z_0 = f('\ndef ')
  test_result_0 = y_0 == z_0
  if not test_result_0:
    print(f'y: {y_0}')
    print(f'z: {z_0}')

  y_1 = '\n\n  def '
  z_1 = f('\n  def ')
  test_result_1 = y_1 == z_1
  if not test_result_1:
    print(f'y: {y_1}')
    print(f'z: {z_1}')

  y_2 = 'abc'
  z_2 = f('abc')
  test_result_2 = y_2 == z_2
  if not test_result_2:
    print(f'y: {y_2}')
    print(f'z: {z_2}')

  return all([test_result_0, test_result_1, test_result_2])
