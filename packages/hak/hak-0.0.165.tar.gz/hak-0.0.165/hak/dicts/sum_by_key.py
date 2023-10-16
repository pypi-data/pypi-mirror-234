from hak.pxyz import f as pxyz

# f_sum
f = lambda x, k: sum(_[k] for _ in x)

def t():
  x = [
    {'name': 'Cash', 'amount': 194},
    {'name': 'Accounts Receivable', 'amount': 120},
    {'name': 'Supplies (Petrol)', 'amount': 10},
    {'name': 'Lawnmower', 'amount': 195},
    {'name': 'Petrol can', 'amount': 15},
  ]
  k = 'amount'
  y = 534
  z = f(x, k)
  return pxyz(x, y, z)
