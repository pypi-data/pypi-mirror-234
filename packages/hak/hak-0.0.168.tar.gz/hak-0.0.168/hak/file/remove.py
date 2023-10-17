from os.path import exists
from os import remove

from hak.file.save import f as save

def f(filepath):
  if exists(filepath): remove(filepath)
  return filepath

temp_file_path = './_.txt'

up = lambda: save(temp_file_path, 'xyz')

def t():
  up()
  z = f(temp_file_path)
  return all([not exists(temp_file_path), z == temp_file_path])
