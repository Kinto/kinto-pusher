#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

requirements = [
    'kinto>=3.0.0',
    'pusher'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='kinto-pusher',
    version='0.6.0',
    description="Plug Kinto notifications into Pusher.com",
    long_description=readme + '\n\n' + history,
    author="Mathieu Leplatre",
    author_email='mathieu@leplat.re',
    url='https://github.com/Kinto/kinto-pusher',
    packages=[
        'kinto_pusher',
    ],
    package_dir={'kinto_pusher':
                 'kinto_pusher'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License (2.0)",
    zip_safe=False,
    keywords='kinto pusher',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
