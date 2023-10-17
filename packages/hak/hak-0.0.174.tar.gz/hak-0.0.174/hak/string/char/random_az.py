from string import ascii_lowercase
from random import choice as tj

f = lambda: tj(ascii_lowercase)
t = lambda: f() in ascii_lowercase
