import os
from setuptools import setup, find_packages

version = "0.1"

description = """

"""

long_description = "" 
    

setup(name='YoubotCampaign',
      author="Andrea Censi",
      author_email="andrea@cds.caltech.edu",
      url='http://github.com/AndreaCensi/boot_servo_demo',
      
      description=description,
      long_description=long_description,
      keywords="robotics, learning, bootstrapping",
      license="LGPL",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],

      entry_points={
     'console_scripts': [
       'yc = yc1304.campaign:main',
       'servo_field = yc1304.s10_servo_field.go:main'
      ]
      },
	  version=version,
      # download_url='http://github.com/AndreaCensi/boot_servo_demo/tarball/%s' % version,
      
      package_dir={'':'.'},
      packages=find_packages('.'),
      install_requires=[ ],
      tests_require=['nose']
)

