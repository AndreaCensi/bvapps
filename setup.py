from setuptools import find_packages, setup
import os

version = "1.0"

description = """"""

long_description = description

setup(name='bvapps',
      url='http://github.com/AndreaCensi/bvapps/',

      description=description,
      long_description=long_description,
      keywords="",
      license="LGPL",

      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      ],

      version=version,
      download_url='http://github.com/AndreaCensi/bvapps/tarball/%s' % version,

      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[
        'BootOlympics',
        'PyVehicles',
        'BootAgents',
      ],
      extras_require={},
      setup_requires=['nose>=1.0'],
      tests_require=[
        'nose>=1.0', 
        'comptests',
       ],

      entry_points={
      },
      test_suite='nose.collector',
)

