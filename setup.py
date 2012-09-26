#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-generic-permissions',
    version='0.0.1',
    description='A generic permission framework for Django',
    author='Garry Polley',
    author_email='garrympolley@gmail.com',
    url='https://github.com/garrypolley/django_generic_permissions',
    packages=find_packages(exclude=('tests', 'examples')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.4'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
