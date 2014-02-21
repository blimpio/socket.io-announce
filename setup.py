#!/usr/bin/env python
import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()


setup(
    name='socket.io-announce',
    version='0.0.1',
    author='Giovanni Collazo',
    author_email='hello@gcollazo.com',
    description='Socket.io multi-process announcement channel ported to Python',
    license='MIT',
    keywords='websockets nodejs socket.io socketio',
    url='http://github.com/gcollazo/socket.io-announce',
    packages=['announce'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    test_suite='tests.test_announce')
