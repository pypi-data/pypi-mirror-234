#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='python-libtiepie-bi',
      version='1.1.11',
      description='Python bindings for LibTiePie',
      license='MIT',
      author='TiePie engineering',
      author_email='support@tiepie.nl',
      url='https://github.com/hennjanssen/python-libtiepie-bi',
      packages=find_packages(include=['libtiepie', 'libtiepie.*']),
      package_data={'libtiepie': ['_platform/*/*/*.dll', '_platform/*/*/*.so*']},
      python_requires='>=3',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows :: Windows 10',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development',
      ])
