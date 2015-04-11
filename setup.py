"""
Flask-SQLAlchemy-Session
-----------------------

Provides an SQLAlchemy scoped session that creates
unique sessions per Flask request
"""
from setuptools import setup

setup(name="Flask-SQLAlchemy-Session",
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
