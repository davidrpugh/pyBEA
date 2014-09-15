from setuptools import setup, find_packages

setup(name='pybea',
      packages=find_packages(exclude=['pybea.tests']),
      version='0.1.0',
      description='Python package for accessing data from the BEA data API',
      author='David R. Pugh',
      author_email='david.pugh@maths.ox.ac.uk',
      url='https://github.com/davidrpugh/pyBEA',
      license='LICENSE.rst',
      install_requires=['json, numpy, pandas, requests'],
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Education',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   ]
      )
