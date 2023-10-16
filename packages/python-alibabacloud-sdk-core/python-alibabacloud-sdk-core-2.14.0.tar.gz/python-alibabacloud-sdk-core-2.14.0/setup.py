#!/usr/bin/python

import os
import sys

from setuptools import setup, find_packages

"""

"""

PACKAGE = "aliyunsdkcore"
DESCRIPTION = "The core module of Aliyun."
AUTHOR = "wangshan"
AUTHOR_EMAIL = ""
URL = ""

TOPDIR = os.path.dirname(__file__) or "."
VERSION = __import__(PACKAGE).__version__

with open("README.rst") as fp:
    LONG_DESCRIPTION = fp.read()

requires = [
    "jmespath>=0.9.3,<1.0.0",
    "cryptography>=2.6.0"
]

setup_args = {
    'version': VERSION,
    'description': DESCRIPTION,
    'long_description': LONG_DESCRIPTION,
    'author': AUTHOR,
    'author_email': AUTHOR_EMAIL,
    'license': "Apache License 2.0",
    'url': URL,
    'packages': find_packages(exclude=["tests*"]),
    'package_data': {'aliyunsdkcore': ['data/*.json', '*.pem', "vendored/*.pem"],
                     'aliyunsdkcore.vendored.requests.packages.certifi': ['cacert.pem']},
    'platforms': 'any',
    'install_requires': requires,
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

setup(name='python-alibabacloud-sdk-core', **setup_args)
