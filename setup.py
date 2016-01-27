import os

from distutils.core import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Education',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Topic :: Scientific/Engineering',
               ]

DESCRIPTION = "Python package for accessing data from the BEA data API"

PACKAGES = ['pybea', 'pybea.tests']

setup(name='pybea',
      packages=PACKAGES,
      version='0.2.0-alpha',
      description=DESCRIPTION,
      author='David R. Pugh',
      author_email='david.pugh@maths.ox.ac.uk',
      url='https://github.com/davidrpugh/pyBEA',
      license='LICENSE.rst',
      classifiers=CLASSIFIERS
      )
