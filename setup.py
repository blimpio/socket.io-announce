#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import re
import sys


name = 'socket.io-announce'
package = 'announce'
author = 'Giovanni Collazo'
author_email = 'hello@gcollazo.com'
description = 'Socket.io multi-process announcement channel ported to Python'
license = 'MIT'
keywords = 'websockets nodejs socket.io socketio'
url = 'https://github.com/GetBlimp/socket.io-announce'
packages = ['announce']
test_suite = 'tests.test_announce'
install_requires = ['redis>=2.9.1']
classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Utilities',
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)

version = get_version(package)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()


# Publish command `python setup.py publish`
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist register upload')
    os.system('python2.7 setup.py bdist_wheel register upload')
    print('===================')
    print('You probably wnat to tag the version now:')
    print('git tag {0}'.format(version))
    print('git push --tags')
    print('===================')
    sys.exit()


setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    license=license,
    keywords=keywords,
    url=url,
    packages=packages,
    install_requires=install_requires,
    long_description=long_description,
    classifiers=classifiers,
    test_suite=test_suite
)
