# hak
This project is a collection of function test pairs for common tasks.
Mostly for my own use but others are welcome to leverage it.

## Required configuration
`git config --global user.email "you@example.com"`
`git config --global user.name "Your Name`
`pip install xgu`

## Required packages
* `sudo apt install twine`

## Test Cycle
`nodemon --exec python3 test.py`

## TODO
- Report empty double lines at end of test cycle
- Report unsorted imports
- Report empty line should follow last import
- Report foreign imports should preceed local imports
- Report unused imports
- Fix test for pxyz
