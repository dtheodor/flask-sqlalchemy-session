# -*- coding: utf-8 -*-
"""
Flask-SQLAlchemy-Session
-----------------------

Provides an SQLAlchemy scoped session that creates
unique sessions per Flask request
"""
import os
from setuptools import setup

# Hard linking doesn't work inside VirtualBox shared folders. This means that
# you can't use tox in a directory that is being shared with Vagrant,
# since tox relies on `python setup.py sdist` which uses hard links. As a
# workaround, disable hard-linking if setup.py is a descendant of /vagrant.
# See
# https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
# for more details.
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link

setup(
    name="Flask-SQLAlchemy-Session",
    version="1.0",
    packages=["flask_sqlalchemy_session"],
    author="Dimitris Theodorou",
    author_email="dimitris.theodorou@gmail.com",
    url='http://github.com/dtheodor/flask-sqlalchemy-session',
    license="MIT",
    description='SQL Alchemy session scoped on Flask requests.',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=["sqlalchemy>=0.9", "Flask>=0.9", "Werkzeug>=0.6.1"],
    tests_require=["pytest>=2.6", "mock>=1.0"],
    extras_require={
        'docs': ["Sphinx>=1.2.3", "alabaster>=0.6.3"]
    }
)
