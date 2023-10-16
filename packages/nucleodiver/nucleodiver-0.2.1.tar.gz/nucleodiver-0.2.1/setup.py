#!/usr/bin/env python
from setuptools import setup, find_packages
from nucleodiver.__init__ import __version__

setup(name='nucleodiver',
      version=__version__,
      description='Calculate nucleotide diverity from VCF.',
      author='Koki Chigira',
      author_email='s211905s@st.go.tuat.ac.jp',
      url='https://github.com/KChigira/nucleodiver/',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'pandas',
      ],
      entry_points={'console_scripts': [
            'nucleodiver = nucleodiver.nucleodiver_4:main',
            'calcpie = nucleodiver.calcpie:main',
            ]
      }
    )
