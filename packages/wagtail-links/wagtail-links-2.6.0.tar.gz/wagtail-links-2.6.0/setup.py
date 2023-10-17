#!/usr/bin/env python
from setuptools import setup, find_packages, Distribution
import codecs
import os.path

# Make sure versiontag exists before going any further
Distribution().fetch_build_eggs("versiontag>=1.2.0")

from versiontag import get_version, cache_git_tag  # NOQA


packages = find_packages("src")

install_requires = [
    "wagtail>=4.1,<6.0",
]

extras_require = {
    "development": [
        "flake8>=3.3.0",
        "tox>=2.7.0",
        "versiontag>=1.2.0",
    ],
}


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding="utf-8").read()


cache_git_tag()

setup(
    name="wagtail-links",
    description="Wagtail links provides a consistent way to refer to links in a wagtail page.",
    version=get_version(pypi=True),
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="django wagtail",
    author="thelabnyc",
    author_email="thelabdev@thelabnyc.com",
    url="https://gitlab.com/thelabnyc/wagtail-links",
    license="ISC",
    package_dir={"": "src"},
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
)
