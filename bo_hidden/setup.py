import os
from setuptools import setup, find_packages

version = "1.0"

description = """Experiments with hidden state""" 

    
long_description = description  

setup(name='BOHidden',
      url='',
      
      description=description,
      long_description=description,
      keywords="", # XXX
      license="GPL",
      
      classifiers=[
        'Development Status :: 4 - Beta', 
      ],

      version=version,
      
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[ 
        'BootOlympics[compmake]>=1.0,<2', 
        'PyVehicles[procgraph,boot]>=1.0,<2',
      ],
      extras_require={
        # 'videos':  ['PyVehicles[procgraph]'],
      },
      tests_require=['nose'],
      entry_points={
         'console_scripts': [
           'bo_hidden_main = '
                'bo_hidden.go:main',
        ]
      }          
)

