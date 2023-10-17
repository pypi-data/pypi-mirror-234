from hak.file.save import f as save
from hak.file.load import f as load
from hak.file.remove import f as remove
from hak.file.decrypt import f as decrypt
from subprocess import run

_content = "Dyson Sphere\n"
_in_filename = "./_test_file_encrypt_in.txt"
_enc_filename = "./_test_file_encrypt_in.txt.enc"
_out_filename = "./_test_file_encrypt_out.txt"
_password = "goldilocks"

def f(in_filename, out_filename, password): run(
  args=[
    "openssl", "enc",
    "-aes-256-cbc",
    "-salt",
    "-pass", f"pass:{password}",
    "-in", f"{in_filename}",
    "-out", f"{out_filename}"
  ],
  capture_output=True
)

def up():
  dn()
  save(_in_filename, _content)

def dn():
  remove(_in_filename)
  remove(_enc_filename)
  remove(_out_filename)

def t():
  up()
  f(_in_filename, _enc_filename, _password)
  decrypt(_enc_filename, _out_filename, _password)
  z = load(_out_filename)
  result = z == _content
  dn()
  return result
