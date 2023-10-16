from hak.file.save import f as st
from hak.file.save_lines import f as sl
from hak.file.save import t as test_string_path
from hak.file.save_lines import t as test_lines_path

f = lambda path, data: (sl if isinstance(data, list) else st)(path, data)

t = lambda: all([test_string_path(), test_lines_path()])
