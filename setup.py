#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name='pygeckodriver',
    # TODO: sync version with Chrome Driver
    version=version,
    author='Park Lam',
    author_email='lqmonline@gmail.com',
    description='A package to sync gecko driver to lastest version',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/parklam/pygeckodriver',
    #packages=setuptools.find_packages(),
    packages=['pygeckodriver'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    keywords='geckodriver gecko firefox driver',
)
