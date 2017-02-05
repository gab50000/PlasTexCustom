from setuptools import setup

setup(name='custex',
      version='0.1',
      description='Custom PlasTeX',
      author='Gabriel Kabbe',
      author_email='gabriel.kabbe@mail.de',
      license='GPLv3',
      packages=['plastexcustom',
                'plastexcustom.packages'],
      install_requires=[],
      entry_points={
                    'console_scripts': ["custex=plastexcustom.main:main",
                                        "prettify=plastexcustom.make_pretty:main"
                                        ],
      },
      zip_safe=False)

