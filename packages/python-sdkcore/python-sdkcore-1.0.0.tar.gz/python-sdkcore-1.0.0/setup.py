#!/usr/bin/python

from setuptools import setup, find_packages
PACKAGE = "aliyunsdkcore"
DESCRIPTION = "sdk core"
VERSION = '1.0.0'


setup_args = {
    'version': VERSION,
    'description': DESCRIPTION,
    'license': "Apache License 2.0",
    'packages': find_packages(exclude=["tests*"]),
    'platforms': 'any',
    'classifiers': (
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    )
}

setup(name='python-sdkcore', **setup_args)
