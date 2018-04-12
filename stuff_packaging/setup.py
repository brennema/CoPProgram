from setuptools import setup

setup(name='CoPProgram',
      version='0.1',
      description='Perform CofP Analysis',
      url='https://github.com/brennema/CoPProgram',
      author='Elora Brenneman, Anthony Gatti',
      author_email='brennema@mcmaster.ca',
      license='MIT',
      packages=['CoPProgram'],
      install_requires=[
      	'numpy',
      	'EMD-signal',
      	'pandas',
      	'matplotlib',
      ],
      dependency_links=['https://github.com/neuropsychology/NeuroKit.py/zipball/master'],
      zip_safe=False)