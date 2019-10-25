from setuptools import setup
with open('README.md') as f:
    readme = f.read()
setup(name='oatspower',
      version='0.3.4',
      description='OATS: Optimisation and Analysis Toolbox for Power Systems',
      long_description=readme,
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
