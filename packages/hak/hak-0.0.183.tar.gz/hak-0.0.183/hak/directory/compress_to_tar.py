from hak.directory.make import f as mkdirine
from hak.directory.remove import f as rmdirie
from hak.file.save import f as save
from subprocess import run
from hak.file.tar.extract import f as extract_tar
from hak.file.load import f as load

_dir_name = './_test_directory_compress_to_tar'
_source = f'{_dir_name}/source'
_source_file_a_path = f'{_source}/a.txt'
_source_file_a_content = "_source_file_a_path"
_source_file_b_path = f'{_source}/b.txt'
_source_file_b_content = "_source_file_b_path"
_compressed_filename = '_compressed.tar.gz'
_compressed_filepath = f'{_dir_name}/{_compressed_filename}'

def up():
  dn()
  mkdirine(_dir_name)
  mkdirine(_source)
  save(_source_file_a_path, _source_file_a_content)
  save(_source_file_b_path, _source_file_b_content)

def dn():
  rmdirie(_dir_name)
  rmdirie(_source)
  rmdirie(_source_file_a_path)
  rmdirie(_source_file_a_content)
  rmdirie(_source_file_b_path)
  rmdirie(_source_file_b_content)

def f(source_directory_path, compressed_filename):
  if not compressed_filename.endswith(".tar.gz"):
    compressed_filename += ".tar.gz"

  _args=f"tar -zcvf {compressed_filename} {source_directory_path}".split()
  result = run(args=_args, capture_output=True)

def t():
  up()
  z = f(source_directory_path=_source, compressed_filename=_compressed_filepath)

  extract_tar(_compressed_filename, _dir_name)

  result = all([
    load(f'{_source_file_a_path}') == load(f'{_dir_name}/source/a.txt'),
    load(f'{_source_file_b_path}') == load(f'{_dir_name}/source/b.txt')
  ])

  dn()
  return result
