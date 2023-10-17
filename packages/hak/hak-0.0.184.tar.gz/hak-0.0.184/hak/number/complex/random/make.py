from random import randint as u
from hak.number.complex.is_a import f as is_complex

f = lambda r_a, r_b, j_a, j_b: u(r_a, r_b) +  u(j_a, j_b)*1j

t = lambda: is_complex(f(**{'r_a': -10, 'r_b': 10, 'j_a': -10, 'j_b': 10}))
