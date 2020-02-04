from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(name='oatspower',
      version='1.0.2',
      description='OATS: Optimisation and Analysis Toolbox for Power Systems',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/bukhsh/oats',
      author='Waqquas Bukhsh',
      author_email='wbukhsh@gmail.com',
      license='GPLv3+',
      packages=['oats','oats.models','oats.testcases'],
      package_data={'oats.testcases': ['*']},
      install_requires =[
        'pyomo',
        'tabulate',
        'PyYAML',
        'ipython[notebook]',
        'openpyxl',
        'pymysql',
        'pypyodbc',
        'pyro4',
        'sympy',
        'xlrd',
        'pandas',
      ],
      zip_safe=False)
