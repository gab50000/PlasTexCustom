from setuptools import setup

setup(name='custex',
      version='0.1',
      description='Custom PlasTeX',
      author='Gabriel Kabbe',
      author_email='gabriel.kabbe@mail.de',
      license='GPLv3',
      packages=['plastexcustom'],
      install_requires=[],
      entry_points={
                    'console_scripts': ["custex=plastexcustom.main:main",
                                        ],      
      },
      zip_safe=False)

