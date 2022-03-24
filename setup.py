"""
This test file is part of the openPMD-CCD.

Copyright 2020 openPMD contributors
Authors: Axel Huebl
License: BSD-3-Clause-LBNL
"""
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('./requirements.txt') as f:
    install_requires = [line.strip('\n') for line in f.readlines()]

# Read the version number, by executing the file openpmd_viewer/__version__.py
# This defines the variable __version__
with open('./openpmd_ccd/__version__.py') as f:
    exec( f.read() )

# Define a custom class to run the tests with `python setup.py test`
class PyTest(TestCommand):
    def run_tests(self):
        import pytest
        errcode = pytest.main([])
        sys.exit(errcode)

# Main setup command
setup(name = 'openPMD-CCD',
      version = __version__,
      description = 'Visualization tools for openPMD files',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      maintainer = 'Axel Huebl',
      maintainer_email = 'axelhuebl@lbl.gov',
      keywords = ('openPMD openscience hdf5 research '
                  'file-format file-handling CCD imaging'),
      url = 'https://github.com/openPMD/openPMD-CCD.git',
      project_urls = {
          # 'Documentation': 'https://[...].readthedocs.io',
          # 'Reference': 'https://doi.org/[...]',
          'Source': 'https://github.com/openPMD/openPMD-CCD',
          'Tracker': 'https://github.com/openPMD/openPMD-CCD/issues',
      },
      # zip_safe = True,
      python_requires = '>=3.6',
      install_requires = install_requires,
      tests_require = ['pytest', 'pytest-datafiles'],
      cmdclass = {'test': PyTest},
      platforms = 'any',
      classifiers = [
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Natural Language :: English',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Database :: Front-Ends',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          ('License :: OSI Approved :: '
           'Lawrence Berkeley National Labs BSD variant license '
           '(BSD-3-Clause-LBNL)'),
    ],
)

