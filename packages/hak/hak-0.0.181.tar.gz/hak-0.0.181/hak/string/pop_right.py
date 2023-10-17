from hak.pxyf import f as pxyf

# def f(x): return (x[:len(x)-1], x[len(x)-1:])
f = lambda x: (x[:len(x)-1], x[len(x)-1:])
t = lambda: pxyf('abc', ('ab', 'c'), f)
