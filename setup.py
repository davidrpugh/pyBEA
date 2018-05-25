import setuptools
from distutils.core import setup


CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Education',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.6',
               'Topic :: Scientific/Engineering',
               ]

DESCRIPTION = "Python package for accessing data from the BEA data API"

PACKAGES = ['pybea']

VERSION = "0.6.0-alpha"

setup(name='pybea',
      packages=PACKAGES,
      version=VERSION,
      description=DESCRIPTION,
      author='David R. Pugh',
      author_email='drpugh@protonmail.com',
      url='https://github.com/davidrpugh/pyBEA',
      license='LICENSE.rst',
      classifiers=CLASSIFIERS
      )
