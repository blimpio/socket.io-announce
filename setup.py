#!/usr/bin/env python
import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()


setup(
    name='socket.io-announce',
    version='0.0.3',
    author='Giovanni Collazo',
    author_email='hello@gcollazo.com',
    description='Socket.io multi-process announcement channel ported to Python',
    license='MIT',
    keywords='websockets nodejs socket.io socketio',
    url='https://github.com/GetBlimp/socket.io-announce',
    packages=['announce'],
    install_requires=[
        'redis>=2.9.1',
    ],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    test_suite='tests.test_announce')
