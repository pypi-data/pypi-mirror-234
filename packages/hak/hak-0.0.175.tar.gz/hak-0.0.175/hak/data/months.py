from hak.strings.get_first_3_chars_of_each import f as f_first_3_chars
from hak.strings.lower_all import f as f_lower_all
from hak.strings.entitle_all import f as f_title_all
from hak.strings.upper_all import f as f_upper_all

# months
months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]

extended_names_as_list = [
  *f_first_3_chars(months),
  *f_first_3_chars(f_lower_all(months)),
  *f_first_3_chars(f_title_all(months)),
  *f_first_3_chars(f_upper_all(months)),
  *f_lower_all(months),
  *f_title_all(months),
  *f_upper_all(months),
]

extended_names_as_set = set(extended_names_as_list)
