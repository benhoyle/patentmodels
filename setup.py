# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='patentmodels',
    version='0.0.1',
    description='Functions and datamodels for patent data.',
    long_description=readme,
    author='Ben Hoyle',
    author_email='benjhoyle@gmail.com',
    url='https://github.com/benhoyle/patentmodels',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
    # packages=['patentmodels']
)
