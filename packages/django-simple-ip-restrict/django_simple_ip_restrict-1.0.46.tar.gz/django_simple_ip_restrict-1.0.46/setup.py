#!/usr/bin/env python3

from io import open

from setuptools import find_packages, setup


def readall(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


setup(
    name="django_simple_ip_restrict",
    version="1.0.46",
    description="Apply an IP restriction to specific routes",
    long_description=readall("README.md"),
    long_description_content_type="text/markdown",
    author="STITCH (Aleksey Panov, Mario Brito, Daniel Hengeveld, André Pereira, Kellie English)",
    author_email="panovitch@gmail.com",
    packages=find_packages(exclude=("tests.*", "tests")),
    python_requires=">=3.5",
    install_requires=["Django>=2.2", "netaddr"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
