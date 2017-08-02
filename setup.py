from setuptools import setup

setup(name='custex',
      version='0.1',
      description='Customized PlasTeX',
      author='Gabriel Kabbe',
      author_email='gabriel.kabbe@mail.de',
      license='GPLv3',
      packages=['plastexcustom',
                'plastexcustom.packages'],
      install_requires=["plasTeX",
                        "pytest",
                        "lxml"],
      entry_points={
                    'console_scripts': ["tex2xml=plastexcustom.main:main",
                                        "prettify=plastexcustom.make_pretty:main",
                                        "treeview=plastexcustom.TexTree:main",
                                        "mktest=plastexcustom.make_test:main"
                                        ],
      },
      zip_safe=False)

