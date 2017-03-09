# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='patentmodels',
    version='0.0.4',
    description='Functions and datamodels for patent data.',
    long_description=readme,
    author='Ben Hoyle',
    author_email='benjhoyle@gmail.com',
    url='https://github.com/benhoyle/patentmodels',
    license='MIT',
    install_requires=['nltk'],
    packages=find_packages(exclude=('tests', 'docs'))
    # packages=['patentmodels']
)
