#!/usr/bin/env python

import sys

from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='rps-milea-framework',
    version='0.0.6',
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    url='https://github.com/red-pepper-services/rps-milea-framework',
    license='MIT',
    description="Django rps.Milea Framework",
    long_description=long_description,
    include_package_data=True,
    install_requires=[
        'Django>=4.1',
        'django-admin-sortable2>=2.1.4',
        'django-cust-email-user>=0.1.2',
        'django-object-actions>=4.1.0',
        'django-currentuser>=0.6.1',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
#