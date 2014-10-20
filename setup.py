#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.md').read()
requirements = [
    'genshi'
]
test_requirements = [
    'nose'
]

setup(
    name='papi',
    version='0.0.1',
    description='Python API documentation generator',
    long_description=readme,
    author='Milan Milanov',
    author_email='whizzer.me@gmail.com',
    url='https://github.com/milanov/papi',
    packages=[
        'papi',
    ],
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    scripts=['bin/papi-cli.py'],
    keywords='documentation, generator, api, docs',
    classifiers=[
    ],
    test_suite='tests',
    tests_require=test_requirements
)