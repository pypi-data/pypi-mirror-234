from datetime import date
from datetime import timedelta as td

from hak.date.is_monday import f as is_monday
from hak.date.is_sunday import f as is_sunday
from hak.date.year.easter_sunday.get import f as get_easter_sunday
from hak.pf import f as pf
from hak.pxyf import f as pxyf

def f(x):
  easter = get_easter_sunday(x.year)
  if x.month == 1 and x.day == 1: return 1
  if all([is_sunday(x-td(1)), x.month == 1, x.day == 2]): return 1
  if x.month == 1 and x.day == 26: return 1
  if x.month == 3 and x.day == 13: return 1
  if easter -td(2) == x: return 1
  if easter -td(1) == x: return 1
  if easter == x: return 1
  if easter +td(1) == x: return 1
  if x.month == 4 and x.day == 25: return 1
  if all([x.month == 5, is_monday(x), x.day >= 27]): return 1
  if all([x.month == 6, is_monday(x), 7 < x.day <= 14]): return 1
  if all([x.month == 10, is_monday(x), x.day <= 7]): return 1
  if all([x.month == 12, x.day == 25]): return 1
  if all([x.month == 12, x.day == 26]): return 1
  return 0

# Wed 25 Jan 2023
t_not_public_holiday_a = lambda: pxyf(date(2023,  1, 25), 0, f)

# Sun 1 Jan 2023
t_new_years_day_act    = lambda: pxyf(date(2023,  1,  1), 1, f)

# Mon 2 Jan 2023
t_new_years_day_obs    = lambda: pxyf(date(2023,  1,  2), 1, f)

# Australia Day	Thu 26 Jan 2023
t_australia_day        = lambda: pxyf(date(2023,  1, 26), 1, f)

# Canberra Day	Mon 13 Mar 2023
t_canberra_day         = lambda: pxyf(date(2023,  3, 13), 1, f)

# Good Friday 7 April 2023
t_good_friday          = lambda: pxyf(date(2023,  4,  7), 1, f)

# Easter Sat – the day after Good Friday	Sat 8 April 2023
t_easter_saturday      = lambda: pxyf(date(2023,  4,  8), 1, f)

# Easter Sun 9 April 2023
t_easter_sunday        = lambda: pxyf(date(2023,  4,  9), 1, f)

# Easter Mon 10 April 2023
t_easter_monday        = lambda: pxyf(date(2023,  4, 10), 1, f)

# ANZAC Day	Tuesday 25 April 2023
t_anzac_day            = lambda: pxyf(date(2023,  4, 25), 1, f)

# Wednesday 28 May 2023
t_not_public_holiday_b = lambda: pxyf(date(2023,  5, 28), 0, f) 

t_not_public_holiday_c = lambda: pxyf(date(2023,  5, 22), 0, f)

# Reconciliation Day	Monday 29 May 2023**
t_reconciliation_day   = lambda: pxyf(date(2023,  5, 29), 1, f)

t_not_public_holiday_d = lambda: pxyf(date(2023,  6, 5), 0, f)

t_not_public_holiday_e = lambda: pxyf(date(2023,  6, 19), 0, f)

# Sovereign's Birthday	Monday 12 June 2023
t_sovereigns_birthday  = lambda: pxyf(date(2023,  6, 12), 1, f)

t_not_public_holiday_f = lambda: pxyf(date(2023, 10,  9), 0, f)

# Labour Day	Monday 2 October 2023
t_labour_day           = lambda: pxyf(date(2023, 10,  2), 1, f)

# Christmas Day	Monday 25 December 2023
t_christmas_day        = lambda: pxyf(date(2023, 12, 25), 1, f)

# Boxing Day	Tuesday 26 December 2023
t_boxing_day           = lambda: pxyf(date(2023, 12, 26), 1, f)

def t():
  if not t_anzac_day():            return pf('!t_anzac_day')
  if not t_australia_day():        return pf('!t_australia_day')
  if not t_boxing_day():           return pf('!t_boxing_day')
  if not t_canberra_day():         return pf('!t_canberra_day')
  if not t_christmas_day():        return pf('!t_christmas_day')
  if not t_easter_monday():        return pf('!t_easter_monday')
  if not t_easter_saturday():      return pf('!t_easter_saturday')
  if not t_easter_sunday():        return pf('!t_easter_sunday')
  if not t_good_friday():          return pf('!t_good_friday')
  if not t_labour_day():           return pf('!t_labour_day')
  if not t_new_years_day_act():    return pf('!t_new_years_day_act')
  if not t_new_years_day_obs():    return pf('!t_new_years_day_obs')
  if not t_not_public_holiday_a(): return pf('!t_not_public_holiday_a')
  if not t_not_public_holiday_b(): return pf('t_not_public_holiday_b')
  if not t_not_public_holiday_c(): return pf('t_not_public_holiday_c')
  if not t_not_public_holiday_d(): return pf('t_not_public_holiday_d')
  if not t_not_public_holiday_e(): return pf('t_not_public_holiday_e')
  if not t_not_public_holiday_f(): return pf('t_not_public_holiday_f')
  if not t_reconciliation_day():   return pf('!t_reconciliation_day')
  if not t_sovereigns_birthday():  return pf('!t_sovereigns_birthday')
  return 1
