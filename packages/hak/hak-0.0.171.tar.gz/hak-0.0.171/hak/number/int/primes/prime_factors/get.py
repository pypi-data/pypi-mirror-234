from collections import deque
from math import ceil
from math import sqrt
from os.path import exists

from hak.file.get_next_line_as_int import f as get_next_prime
from hak.file.zip.extract import f as extract
from hak.number.int.primes.download_prime_10 import f as download_prime_10
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def build_freq_dict(x, primes):
  queue = deque([1, *primes])
  p = queue.pop()
  result = {}
  while queue:
    if x//p == x/p:
      result[p] = (result[p] + 1) if p in result else 1
      x /= p
    else:
      p = queue.pop()
  return result

def f(x):
  _x = x
  if not exists('primes10.txt'):
    if not exists('prime10.zip'):
      download_prime_10()
    extract("prime10.zip", './')

  limit = ceil(sqrt(abs(_x)))
  p = 2
  prime_factors_set = set()
  with open('primes10.txt', 'r') as file:
    while p <= limit:
      p = get_next_prime(file)
      if not _x % p:
        _x = _x // p
        prime_factors_set.add(p)
  
  prime_factors_list = tuple(sorted(list(prime_factors_set), reverse=True))
  return build_freq_dict(x, prime_factors_list)


t_7093094658085993 = lambda: pxyf(
  7093094658085993,
  {71: 1, 1109: 1, 33757: 1, 2668591: 1},
  f
)

def t():
  if not pxyf(2, {2: 1}, f): return pf('!t_2')
  if not pxyf(3, {3: 1}, f): return pf('!t_3')
  if not pxyf(4, {2: 2}, f): return pf('!t_4')
  if not pxyf(10, {2: 1, 5: 1}, f): return pf('!t_10')
  if not pxyf(360, {2: 3, 3: 2, 5: 1}, f): return pf('!t_360')
  if not t_7093094658085993(): return pf('!t_7093094658085993')
  return 1
