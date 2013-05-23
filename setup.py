#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "rtl_django_tools",
    version = "0.0.1",
    author = "ReThought Ltd",
    author_email = "code@rethought-solutions.com",
    url = "https://github.com/rethought/rtl_django_tools.git",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    license = "BSD",
    keywords = "django, utilities, users, usermodel",
    description = "Custom models and utilities for Django, including User "
                  "models that key on email address and remove username",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
