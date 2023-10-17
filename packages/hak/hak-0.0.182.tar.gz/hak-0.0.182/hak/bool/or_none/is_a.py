f = lambda x: isinstance(x, bool) or x is None

t = lambda: all([not any([f('a'), f(0), f(1)]), f(True), f(False), f(None)])
