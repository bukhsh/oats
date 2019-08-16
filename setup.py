from setuptools import setup

setup(name='oatspower',
      version='0.0.1',
      description='OATS: Optimisation and Analysis Toolbox for Power Systems',
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
        'ipopt'
      ],
      zip_safe=False)
