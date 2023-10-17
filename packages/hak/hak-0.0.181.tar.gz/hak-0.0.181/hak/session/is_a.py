from requests.sessions import Session
from requests import session

f = lambda x: isinstance(x, Session)

t = lambda: f(session()) and not f('a')
