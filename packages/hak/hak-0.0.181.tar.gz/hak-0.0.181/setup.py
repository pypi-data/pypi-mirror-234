from setuptools import setup
from pathlib import Path
from hak.directory.filepaths.packages.get import f as get_packages
long_description = Path("./README.md").read_text()

setup(
  name='hak',
  version='0.0.181',
  license='MIT',
  description='Function Test Pair Toolbox',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='@JohnRForbes',
  author_email='john.robert.forbes@gmail.com',
  url='https://github.com/JohnForbes/hak',
  packages=[_[2:] for _ in list(get_packages('.'))],
  keywords='hak',
  install_requires=[],
)
