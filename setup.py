from setuptools import setup, find_packages
import sys, os

version = '0.9'

setup(name='sitegen',
      version=version,
      description="Site Generator",
      long_description="""\
A generator for creating web pages from templates""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sitegenerator web html generation',
      author='Christian Scholz',
      author_email='cs@comlounge.net',
      url='http://comlounge.net',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "jinja2",
          "quantumcore.resources",
      ],
      entry_points={
        'console_scripts': [
            'sitegen = sitegen.generator:generate',
        ],
      },

      )
