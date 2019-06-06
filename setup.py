#!/usr/bin/env python
import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding="utf-8") as f:
        content = f.read()
    return content


README = read_file("README.rst")
CHANGELOG = read_file("CHANGELOG.rst")

requirements = ["kinto", "pusher"]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name="kinto-pusher",
    version="1.0.0",
    description="Plug Kinto notifications into Pusher.com",
    long_description=README + "\n\n" + CHANGELOG,
    author="Mathieu Leplatre",
    author_email="mathieu@leplat.re",
    url="https://github.com/Kinto/kinto-pusher",
    packages=["kinto_pusher"],
    package_dir={"kinto_pusher": "kinto_pusher"},
    include_package_data=True,
    install_requires=requirements,
    license="Apache License (2.0)",
    zip_safe=False,
    keywords="kinto pusher",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
