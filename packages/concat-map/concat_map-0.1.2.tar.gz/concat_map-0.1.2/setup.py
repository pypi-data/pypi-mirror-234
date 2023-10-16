"""
This setup file is used to package the concat_map module.  The module is
used accessing a collection of array-like objects as if they are a single
array.
"""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='concat_map',
  version='0.1.2',
  author='Gary William Flake',
  author_email='gary@flake.org',
  description=
  'A module for accessing many array-like objects as if they are one array.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_packages(include=['concat_map', 'concat_map.*']),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
)
